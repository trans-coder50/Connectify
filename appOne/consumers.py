import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from appOne.models import Comments
from appOne.models import Profile
from appOne.models import Rooms
from appOne.models import Messages

User = get_user_model()

class appOneConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg1 = received_data.get('message1')
        msg2 = received_data.get('message2')
        sent_by_id = received_data.get('sent_by')
        print(msg2)
        if not msg1:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        
        if not sent_by_user:
            print('Error:: sent by user is incorrect')

        await self.create_chat_message(sent_by_user,msg1,msg2)

        self_user = self.scope['user']
      
        response = {
            'message1': msg1,
            'message2':msg2,
            'sent_by_name': self_user.username,
       
        }

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnect', event)
    @database_sync_to_async
    def get_user_object(self, user_id):
            qs = User.objects.filter(id=user_id)
            if qs.exists():
                obj = qs.first()
            else:
                obj = None
            return obj
    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
 
    @database_sync_to_async
    def create_chat_message(self, user, msg1,msg2):
        Comments.objects.create(username=user, comment=msg1,post=msg2)

class MessagesHandling(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        print(msg)
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        room_id = received_data.get('room')

        if not msg:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        room_obj = await self.get_room(room_id)
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not room_obj:
            print('Error:: Room id is incorrect')

        await self.create_chat_message(room_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'room_id': room_id
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )


    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_room(self, room_id):
        qs = Rooms.objects.filter(id=room_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, room, user, msg):
        Messages.objects.create(room=room, user=user, message=msg)

