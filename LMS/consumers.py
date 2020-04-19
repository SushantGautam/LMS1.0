import json
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
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



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


# from datetime import datetime
# from django.conf import settings
# import os
# import json
# from functools import reduce

# def storeChat(message, room_name):
#     path = settings.MEDIA_ROOT
#     if not os.path.exists(os.path.join(path, 'chatlog')):
#         os.makedirs(os.path.join(path, 'chatlog'))
#     if not os.path.exists(os.path.join(path, 'chatlog/' + room_name)):
#         os.makedirs(os.path.join(path, 'chatlog/' + room_name))
#     data = json.loads(message.content['text'])
#     currenttime = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-4]
#     data['currenttime'] = currenttime
#     # pathfilelist = [path,'chatlog',room_name + '' + currenttime + '.txt']
#     # # pathfile = reduce(os.path.join, pathfilelist)
#     # pathfile = os.path.join(*pathfilelist)
#     # pathfile = path + '/chatlog/' + room_name + '/' + currenttime + '.txt',
#     # print(pathfile)

#     try:
#         if 'chat_message' in data:
#             with open(path + '/chatlog/' + room_name + '/' + currenttime + '.txt', 'w') as outfile:
#                 json.dump(data, outfile, indent=4)
#     except:
#         pass

#     else:
#         return
