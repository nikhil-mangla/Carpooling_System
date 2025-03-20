import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('rides', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('rides', self.channel_name)

    async def ride_created(self, event):
        await self.send(text_data=json.dumps(event['ride']))