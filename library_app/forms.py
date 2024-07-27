from django import forms
from .models import Book,Author,BookShelf,User
from django.contrib.auth.forms import UserCreationForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'summary', 'cover_photo', 'pdf_file', 'author', 'shelf']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['cover_photo'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['pdf_file'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['shelf'].widget.attrs.update({'class': 'form-control'})


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'description']

class BookshelfForm(forms.ModelForm):
    class Meta:
        model = BookShelf
        fields = ['location']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']