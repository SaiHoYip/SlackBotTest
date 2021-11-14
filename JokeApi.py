import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

def joke():
    #https://github.com/sameerkumar18/geek-joke-api
    url = 'https://geek-jokes.sameerkumar.website/api?format=json'
    api_request = requests.get(url)
    data = json.loads(api_request.text)
    return data['joke']

print(joke())