from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, AuthorViewSet, BookShelfViewSet, HistoryViewSet,
    dashboard, home, book_detail, user_login, add_book, edit_book, delete_book,
     approve_request, reject_request, landing, signup, logout_view,manage_requests,
     request_book,add_author,add_shelf,user_history
)
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'bookshelves', BookShelfViewSet)
router.register(r'histories', HistoryViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('login/', user_login, name='login'),
    path('add-book/', add_book, name='add-book'),
    path('book/<int:pk>/edit/', edit_book, name='book-edit'),
    path('book/<int:pk>/delete/', delete_book, name='book-delete'),
    path('manage-requests/', manage_requests, name='manage-requests'),
    path('approve-request/<int:pk>/', approve_request, name='approve-request'),
    path('reject-request/<int:pk>/', reject_request, name='reject-request'),
    path('logout/', logout_view, name='logout'),
    path('landing/', landing, name='landing'),
    path('signup/', signup, name='signup'),
    path('book-requests/<int:pk>/', request_book, name='book-requests'),
    path('add-author/', add_author, name='add-author'),
    path('add-shelf/', add_shelf, name='add-shelf'),
    path('user-history/', user_history, name='user-history'),

]
