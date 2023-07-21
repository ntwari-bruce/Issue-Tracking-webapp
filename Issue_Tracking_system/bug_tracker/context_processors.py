from .models import CustomUser, Notification
from datetime import datetime, timedelta, time
from django.utils import timezone

def my_context_processor(request):
    new_count = 0

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        now = timezone.now()
        threshold = now - timedelta(seconds=60)
        today_notifications = notifications.filter(created_at__gte=threshold)
        new_count = today_notifications.count()

    return {
        'new_count': new_count
    }
