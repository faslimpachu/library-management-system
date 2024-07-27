from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookRequest, History

@receiver(post_save, sender=BookRequest)
def create_or_update_history(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        history, created = History.objects.get_or_create(
            user=instance.user,
            book=instance.book,
            defaults={'borrowed_date': instance.borrowed_at, 'return_date': instance.return_at}
        )
        if not created:
            history.borrowed_date = instance.borrowed_at
            history.return_date = instance.return_at
            history.save()
    elif instance.status == 'returned':
        try:
            history = History.objects.get(user=instance.user, book=instance.book)
            history.return_date = instance.return_at
            history.save()
        except History.DoesNotExist:
            
            pass
