from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_user_set',  # Add this line
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='library_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_user_set',  # Add this line
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='library_user'
    )

class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class BookShelf(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location

class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    cover_photo = models.ImageField(upload_to='cover_photos/')
    pdf_file = models.FileField(upload_to='book_pdfs/', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    shelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)
 
    
    def __str__(self):
        return self.title

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} borrowed {self.book}'


class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    borrowed_at = models.DateTimeField(null=True, blank=True)
    return_at = models.DateTimeField(null=True, blank=True)
     

    def approve(self):
        self.status = 'approved'
        self.borrowed_at = timezone.now()
        self.return_at = self.borrowed_at + timedelta(days=3)
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    def return_book(self):
        self.status = 'returned'
        self.return_at = timezone.now()
        self.save()
