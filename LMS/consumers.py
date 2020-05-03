import json
import os
from datetime import datetime
from pathlib import Path
from .settings import MEDIA_ROOT

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        text_data_json = json.loads(text_data)
        sender_id = text_data_json['sender_id']
        sender_name = text_data_json['sender_name']
        sender_icon = text_data_json['sender_icon']
        sender_datetime = text_data_json['sender_datetime']
        message = text_data_json['message']

        # Calls function to store the chat
        storeChat(text_data_json, self.room_group_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'sender_name': sender_name,
                'sender_icon': sender_icon,
                'sender_datetime': sender_datetime,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender_id = event['sender_id']
        sender_name = event['sender_name']
        sender_icon = event['sender_icon']
        sender_datetime = event['sender_datetime']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'sender_name': sender_name,
            'sender_icon': sender_icon,
            'sender_datetime': sender_datetime,
            'message': message
        }))


# Function to store each chat text in new file inside chapterid folder
def storeChat(data, room_name):
    file_path = os.path.join(MEDIA_ROOT,'chatlog', room_name)

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


# from channels import Group
# import time


# # Connected to websocket.connect
# def ws_job_connect(message, group_id):
#     message.reply_channel.send({"accept": True})
#     Group(group_id).add(message.reply_channel)


# # Connected to websocket.receive
# def ws_message(message, group_id):
#     storeChat(message, group_id)
#     Group(group_id).send({
#         "text": "%s" % message.content['text'],
#     })


# # Connected to websocket.disconnect
# def ws_disconnect(message, group_id):
#     Group(group_id).discard(message.reply_channel)



# from django.conf import settings
# from functools import reduce