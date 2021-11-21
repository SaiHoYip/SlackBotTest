import requests
import json

def coffeePic():
    url = 'https://coffee.alexflipnote.dev/random.json'
    api_request = requests.get(url)
    data = json.loads(api_request.text)
    return data['file']
