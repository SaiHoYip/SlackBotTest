import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

def dictionary(word):
    route = f'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
    api_request = requests.get(route)
    data = json.loads(api_request.text)
    definition = data
    sentence = definition[0]['word'] + '\n' + definition[0]['meanings'][0]['definitions'][0]['definition']
    return sentence
