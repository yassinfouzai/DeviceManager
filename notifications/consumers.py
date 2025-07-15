# chat/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Send welcome message immediately
        await self.send_json({"message": "Welcome to the WebSocket!"})

    async def disconnect(self, close_code):
        pass

    async def send_notification(self, event):
        await self.send_json({
            "message": "its working"
        })
