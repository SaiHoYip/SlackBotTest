import requests
import json

#https://jokeapi.dev/
def jokes():
    url = 'https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit'
    api_request = requests.get(url)
    data = json.loads(api_request.text)
    if 'joke' in data:
        return data['joke']
    else: 
        return data['setup'], data['delivery']

print(jokes())
