import requests
import json

def dogPic():
    url = 'https://random.dog/woof.json'
    api_request = requests.get(url)
    data = json.loads(api_request.text)
    return data['url']


