import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import weatherAPI

env_path = Path('.')/ '.env'
load_dotenv(dotenv_path= env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

message_counts = {}
welcome_message = {}
weather = {}

class GreetingMessage:
    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': (
                'Welcome to the channel! \n\n'
                '*Get started through here*'
            )
        }
    }

    DIVIDER = {
        'type' : 'divider'
    }

    def __init__(self,channel,user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False
    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'username': 'Welcome Robot!',
            'icon_emoji': self.icon_emoji,
            'blocks': [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }
    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'
        text = f'{checkmark} *React*'
        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}
    
#Simple Hello Message
def Hello(channel_id, text):
    if text == "fu":
        client.chat_postMessage(channel= channel_id, text="no cursing")
    else:
        client.chat_postMessage(channel= channel_id, text=text)

def send_welcome(channel,user):

    if channel not in welcome_message:
        welcome_message[channel] = {}
    
    welcome = GreetingMessage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp = response['ts']

    welcome_message[channel][user] = welcome
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    #limits the call to users
    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        elif user_id not in message_counts:
            message_counts[user_id] = 1
        if text.lower() == 'start':
            send_welcome(f'@{user_id}', user_id)
        

#WIP
@ slack_event_adapter.on('reaction_added')
def reaction(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')

    if f'@{user_id}' not in welcome_message:
        return
    welcome = welcome_message[f'@{user_id}'][user_id]
    welcome.completed = True
    welcome.channel = channel_id
    message = welcome.get_message()
    updated_message = client.chat_update(**message)
    welcome.timestamp = updated_message['ts']

@app.route('/message-count', methods= ['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"Message:{message_count}")
    return Response(), 200

@app.route('/weather', methods = ['POST'])
def weather():
    return weatherAPI.weather()
if __name__=="__main__":
    app.run(debug=True)
