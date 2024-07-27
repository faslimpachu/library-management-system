from rest_framework import viewsets, permissions
from .models import User, Book, Author, BookShelf, History,BookRequest
from .serializers import UserSerializer, BookSerializer, AuthorSerializer, BookShelfSerializer, HistorySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import BookForm,SignUpForm
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import AuthorForm, BookshelfForm




class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_librarian

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_customer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsLibrarian | IsCustomer]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]

class BookShelfViewSet(viewsets.ModelViewSet):
    queryset = BookShelf.objects.all()
    serializer_class = BookShelfSerializer
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsLibrarian | IsCustomer]
    

def user_login(request):
     if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_librarian:
            return redirect('dashboard')
        else:
            return redirect('home')

     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please provide both username and password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser or user.is_librarian:
                return redirect('dashboard')
            elif user.is_customer:
                return redirect('home')
        else:
            messages.error(request, "Invalid login details provided.")
            return redirect('login')

     return render(request, 'login.html')


def signup(request):
     if request.user.is_authenticated:
        return redirect('home')

     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('signup')

     else:
        form = SignUpForm()
     return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    # if not request.user.is_librarian:
    #     return redirect('home')  
    books = Book.objects.all()
    return render(request, 'dashboard.html', {'books': books})

@login_required
def home(request):
    # if not request.user.is_customer:
    #     return redirect('dashboard') 
    books = Book.objects.all()
    bookshelves = BookShelf.objects.all()
    return render(request, 'home.html', {'books': books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_request = BookRequest.objects.filter(book=book, user=request.user).first()
    context = {
        'book': book,
        'author': book.author,
        'shelf': book.shelf,
        'book_request': book_request,
    }
    return render(request, 'book_detail.html', context)


@login_required
def request_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_request, created = BookRequest.objects.get_or_create(book=book, user=request.user)
    if created:
        book_request.status = 'pending'
        book_request.save()
        messages.success(request, 'Your request has been submitted successfully. Admin will apporove your request soon. Plase refresh the page after 5 minutes')
    else:
        messages.info(request, 'You have already requested this book.')
    return redirect('book-detail', pk=pk)

@login_required
def add_book(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to add books.")
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookForm()
    
    authors = Author.objects.all()
    shelves = BookShelf.objects.all()
    return render(request, 'add_book.html', {'form': form, 'authors': authors, 'shelves': shelves})


@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        author = Author(name=name, description=description)
        author.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def add_shelf(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        shelf = BookShelf(location=location)
        shelf.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to edit books.")
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    authors = Author.objects.all()
    shelves = BookShelf.objects.all()
    return render(request, 'edit_book.html', {'form': form, 'book': book, 'authors': authors, 'shelves': shelves})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to delete books.")
    
    if request.method == 'POST':
        book.delete()
        return redirect('dashboard')
    
    return render(request, 'delete_book.html', {'book': book})




@login_required
def manage_requests(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    requests = BookRequest.objects.all()
    return render(request, 'manage_requests.html', {'requests': requests})

@login_required
def approve_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.approve()
    return redirect('manage-requests')

@login_required
def return_book(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.return_book()
    return redirect('manage-requests')

@login_required
def reject_request(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to reject requests.")
    
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.reject()
    
    return redirect('manage-requests')
    
@login_required
def user_history(request):
    histories = BookRequest.objects.filter(user=request.user)
    return render(request, 'user_history.html', {'histories': histories})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


def landing(request):
    return render (request,'landing.html')