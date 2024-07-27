from django.conf import settings
from cryptography.fernet import Fernet
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from library_app.models import User

class EncryptionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if getattr(settings, 'ENCRYPT_EMAILS', False):
            fernet = Fernet(settings.SECRET_KEY)
            for user in User.objects.all():
                user.email = fernet.encrypt(user.email.encode()).decode()
                user.save()
        return response


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/login') and not request.path.startswith('/signup') and not request.path.startswith('/admin'):
            return redirect('login')
        response = self.get_response(request)
        return response