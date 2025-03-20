import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if user is authenticated
        user = self.scope['user']
        if isinstance(user, AnonymousUser):
            await self.close()
            return
        
        # Use ride-specific group if ride_id is provided, else general 'rides' group
        self.ride_id = self.scope['url_route']['kwargs'].get('ride_id')
        self.group_name = f'ride_{self.ride_id}' if self.ride_id else 'rides'
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def ride_created(self, event):
        await self.send(text_data=json.dumps(event['ride']))