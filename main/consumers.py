import json
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'test_consumer'
        self.group_name = 'test_consumer_group'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': 'Connected!!!'}))

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=json.dumps({'you sent': text_data}))

    def disconnect(self, code):
        print('Disconnected')

    def send_notification(self, event):
        print('event', event)
        self.send(text_data=event.get('value', 'None'))


class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = 'new_consumer'
        self.group_name = 'new_consumer_group'
        await (self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'Connected New Async Json Consumer!!!'}))

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({'you sent': text_data}))

    async def disconnect(self, code):
        print('Disconnected')

    async def send_notification(self, event):
        print('event', event)
        await self.send(text_data=event.get('value', 'None'))
