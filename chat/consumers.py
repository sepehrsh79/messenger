import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from account.models import CustomUser
from .models import Message, UserRoom, Room


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def save_message(self, user, room, message):
        user_room, created = UserRoom.objects.get_or_create(user=user, room=room)
        Message.objects.create(user_room=user_room, content=message)

    @sync_to_async
    def get_user(self, username):
        return CustomUser.objects.get(username=username)

    @sync_to_async
    def get_room(self, code):
        return Room.objects.get(code=code)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        user = await self.get_user(username)
        room = await self.get_room(data['room'])

        await self.save_message(user, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
