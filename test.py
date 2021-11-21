import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import weatherAPI
import JokeApi
import attendence
import CoffeeAPI
import DogAPI
import Dictionary
import NewtonAPi

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

@app.route('/message-count', methods= ['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"Message:{message_count}")
    return Response(), 200

@app.route('/checkin', methods= ['POST'])
def checker():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f"Message")
    return Response(), 200

@app.route('/weather', methods = ['POST'])
def weather():
    data = request.form
    text = data.get('text')
    return weatherAPI.weather(text)

@app.route('/define', methods = ['POST'])
def dictionary():
    data = request.form
    text = data.get('text')
    return Dictionary.dictionary(text)

@app.route('/joke', methods = ['POST'])
def jokeAPI():
    return JokeApi.jokes()

@app.route('/coffee', methods = ['POST'])
def COFFEEAPI():
    return CoffeeAPI.coffeePic()

@app.route('/dog', methods = ['POST'])
def DOGAPI():
    return DogAPI.dogPic()

@app.route('/arithmatic', methods = ['POST'])
def NEWTONAPI():
    data = request.form
    text = data.get('text')
    return NewtonAPi.newton(text)

if __name__=="__main__":
    app.run(debug=True)
