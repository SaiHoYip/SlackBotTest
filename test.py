import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.')/ '.env'
load_dotenv(dotenv_path= env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

#Simple Hello Message
def Hello(channel_id, text):
    if text == "fu":
        client.chat_postMessage(channel= channel_id, text="no cursing")
    else:
        client.chat_postMessage(channel= channel_id, text=text)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    #limits the call to users
    if BOT_ID != user_id:
        Hello(channel_id, text)

@app.route('/message-count', methods= ['POST'])
def message_count():
    return Response, 200
if __name__=="__main__":
    app.run(debug=True)
