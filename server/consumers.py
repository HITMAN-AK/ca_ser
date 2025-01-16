import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from asgiref.sync import sync_to_async
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.other_user = self.scope['url_route']['kwargs']['other_user']

        # Create a shared group name based on both users
        self.room_group_name = f'chat_{min(self.username, self.other_user)}_{max(self.username, self.other_user)}'

        # Join the shared room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send previous messages
        messages = await self.get_messages(self.username, self.other_user)
        for message in messages:
            await self.send(text_data=json.dumps({
                'sen': message.sen,
                'rec': message.rec,
                'mess': message.mess,
                'time': message.time.isoformat()
            }))

    async def disconnect(self, close_code):
        # Leave the shared room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sen = text_data_json['sen']
        rec = text_data_json['rec']
        time = datetime.now()

        # Save the message to the database
        await self.save_message(sen, rec, message, time)

        # Broadcast the message to the shared room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sen': sen,
                'rec': rec,
                'mess': message,
                'time': time.isoformat()
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sen': event['sen'],
            'rec': event['rec'],
            'mess': event['mess'],
            'time': event['time']
        }))

    # Helper methods
    async def get_messages(self, user1, user2):
        from .models import Chat
        return await sync_to_async(
            lambda: list(Chat.objects.filter(
                (Q(sen=user1) & Q(rec=user2)) | (Q(sen=user2) & Q(rec=user1))
            ).order_by('time'))
        )()

    async def save_message(self, sen, rec, message, time):
        from .models import Chat
        await sync_to_async(Chat.objects.create)(sen=sen, rec=rec, mess=message, time=time)
