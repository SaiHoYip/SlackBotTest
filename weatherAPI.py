import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

def weather():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    route = 'http://api.openweathermap.org/data/2.5/weather?q=New%20York&units=imperial&appid=' + api_key
    api_request = requests.get(route)
    data = json.loads(api_request.text)
    sentence = f"It feels like {data['main']['temp']} degrees"
    return sentence
weather()
#response = requests.get(url)
#data = json.loads(response.text)
#print(data)
