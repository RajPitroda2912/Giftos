from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'user_notifications'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from client (if needed)
        pass

    # Add this handler for "new product add" messages
    async def new_product_add(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_product_add',
            'message': event['message'],
            'product_id': event.get('product_id'),
            'product_name': event.get('product_name'),
            'timestamp': datetime.now().isoformat()
        }, cls=DjangoJSONEncoder))

    # Keep your existing send_notification handler
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': event.get('type', 'notification'),
            'message': event['message'],
            'timestamp': event.get('timestamp', datetime.now().isoformat())
        }, cls=DjangoJSONEncoder))