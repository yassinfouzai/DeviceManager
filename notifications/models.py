from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.recipient.username} at {self.timestamp}: {self.content[:40]}"

