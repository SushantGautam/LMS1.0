import json
import os
from datetime import datetime
from pathlib import Path

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

online_users = dict()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # New user added according to room_name
        if self.room_name in online_users.keys():
            online_users[self.room_name].append(self.scope['user'])
        else:
            online_users[self.room_name] = [self.scope['user']]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send message to room group on new user addition
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_users',
                'user_list': messages_to_json(set(online_users[self.room_name])),
            }
        )

    async def disconnect(self, close_code):
        # Remove user according to room_name
        if self.room_name in online_users.keys():
            online_users[self.room_name].remove(self.scope['user'])

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group when user disconnect
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_users',
                'user_list': messages_to_json(set(online_users[self.room_name])),
            }
        )

    # Receive message from connect disconnect
    async def chat_users(self, event):
        user_list = event['user_list']
        user_count = len(user_list)
        
        # Send message to WebSocket about users list
        await self.send(text_data=json.dumps({
            'message_type': 'chat_users',
            'user_list': user_list,
            'user_count': user_count
        }))

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json['sender_id']
        sender_name = text_data_json['sender_name']
        sender_icon = text_data_json['sender_icon']
        sender_datetime = text_data_json['sender_datetime']
        message_type = text_data_json['message_type']
        message = text_data_json['message']

        # Calls function to store the chat
        if message_type == 'chat_message':
            storeChat(text_data_json, self.room_group_name)
        
        chatData = {
            'type': 'chat_message',
            'message_type': message_type,
            'sender_id': sender_id,
            'sender_name': sender_name,
            'sender_icon': sender_icon,
            'sender_datetime': sender_datetime,
            'message': message,
        }
        # message_link_type => determines if message is for quiz or survey. Not present in case of chat messages.
        # if message_link_type present -> 'message' is primary key of quiz or survey
        if 'message_link_type' in text_data_json:
            chatData['message_link_type'] = text_data_json['message_link_type']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            chatData
        )

    # Receive message from room group for chat message
    async def chat_message(self, event):
        sender_id = event['sender_id']
        sender_name = event['sender_name']
        sender_icon = event['sender_icon']
        sender_datetime = event['sender_datetime']
        message_type = event['message_type']
        message = event['message']
        # Send message to WebSocket
        chatdata = {
            'message_type': message_type,
            'sender_id': sender_id,
            'sender_name': sender_name,
            'sender_icon': sender_icon,
            'sender_datetime': sender_datetime,
            'message': message,
        }
        if 'message_link_type' in event:
            chatdata['message_link_type'] = event['message_link_type']
        await self.send(text_data=json.dumps(chatdata))


# Serialization of django queryset
def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result

def message_to_json(message):
    return {
        'id': message.id,
        'username': message.username,
        'fullname': message.getFullName(),
        'avatar':message.Avatar
    }
    

# Function to store each chat text in new file inside chapterid folder
def storeChat(data, room_name):
    file_path = os.path.join(settings.MEDIA_ROOT,'chatlog', room_name)

    Path(file_path).mkdir(parents=True, exist_ok=True)

    currenttime = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-4]
    file_name = currenttime + '.txt'

    try:
        if 'message' in data:
            with open(file_path + '/' + file_name, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        return

    except Exception as e:
        print(e)
        return