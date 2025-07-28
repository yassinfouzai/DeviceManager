from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import sync_to_async
from .models import Notification
from typing import List, Dict, Optional


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def _get_user_notifications_sync(self) -> List[Dict[str, Optional[str]]]:
        notifications_qs = Notification.objects.filter(recipient=self.user).order_by("-timestamp")
        return [
            {
                "id": n.id,
                "message": n.content,
                "timestamp": n.timestamp.isoformat() if n.timestamp else None,
                "read": n.read,
            }
            for n in notifications_qs
        ]
    get_user_notifications = sync_to_async(_get_user_notifications_sync)

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send_json({"message": "WebSocket connected"})

            notifications = await self.get_user_notifications()
            await self.send_json({
                "type": "all_notifications",
                "notifications": notifications,
            })
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send_json({
            "id": event.get("id"),
            "message": event.get("message", "You have a new notification."),
            "timestamp": event.get("timestamp"),
            "read": event.get("read", False)
        })
