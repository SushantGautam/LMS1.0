from channels import Group


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
    data = json.loads(message.content['text'])
    if data['chat_message']:
        with open(path + '/chatlog/' + room_name + '.txt', 'a') as outfile:
            chat_story = {
                "sender_id":data['sender_id'],
                "sender_name": data['sender_name'],
                "sender_icon": data['sender_icon'],
                "message": data['chat_message']
            }
            json.dump(chat_story, outfile, indent=4)
    else:
        return