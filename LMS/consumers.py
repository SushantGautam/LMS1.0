from channels import Group
import time


# Connected to websocket.connect
def ws_job_connect(message, group_id):
    message.reply_channel.send({"accept": True})
    Group(group_id).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message, group_id):
    storeChat(message, group_id)
    Group(group_id).send({
        "text": "%s" % message.content['text'],
    })


# Connected to websocket.disconnect
def ws_disconnect(message, group_id):
    Group(group_id).discard(message.reply_channel)

from datetime import datetime
from django.conf import settings
import os
import json

def storeChat(message, room_name):
    path = settings.MEDIA_ROOT
    if not os.path.exists(os.path.join(path, 'chatlog')):
        os.makedirs(os.path.join(path, 'chatlog'))
    if not os.path.exists(os.path.join(path, 'chatlog/'+room_name)):
        os.makedirs(os.path.join(path, 'chatlog/'+room_name))
    data = json.loads(message.content['text'])
    currenttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    if data['chat_message']:
        with open(path + '/chatlog/' + room_name + '/' + currenttime + '.txt', 'w') as outfile:
            # chat_story = {
            #     "sender_id":data['sender_id'],
            #     "sender_name": data['sender_name'],
            #     "sender_icon": data['sender_icon'],
            #     "chat_message": data['chat_message'],
            #     "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # }
            json.dump(data, outfile, indent=4)
    else:
        return