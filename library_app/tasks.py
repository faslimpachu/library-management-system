from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import BookRequest

@shared_task
def send_due_date_reminders():
    now = timezone.now()
    due_soon_date = now + timedelta(days=1)  
    book_requests = BookRequest.objects.filter(return_at__date=due_soon_date.date(), status='approved')

    for request in book_requests:
        subject = f'Reminder: Book Return Due Soon for {request.book.title}'
        message = (
            f'Dear {request.user.username},\n\n'
            f'This is a reminder that your borrowed book "{request.book.title}" is due for return on {request.return_at.strftime("%Y-%m-%d")}. '
            'Please make sure to return it by the due date to avoid any late fees.\n\n'
            'Thank you!'
        )
        send_mail(subject, message, 'test@gmail.com', [request.user.email])
