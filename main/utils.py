from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification
from django.contrib.auth.models import User


def notify_user(user_id, message):
    try:
        user = User.objects.get(id=user_id)

        notification = Notification.objects.create(
            recipient=user,
            content=message
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_notification",
                "message": message,
                "timestamp": notification.timestamp.isoformat(),
                "id": notification.id,
                "read": notification.read
            }
        )
    except User.DoesNotExist:
        pass


def is_htmx(request):
    return request.headers.get("HX-Request") == "true"
