import requests
import json

def newton(text):
    route = f'https://newton.vercel.app/api/v2/factor/' + text
    api_request = requests.get(route)
    data = json.loads(api_request.text)
    sentence = f"you entered {text} the answer is {data['result']}"
    return sentence