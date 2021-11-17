import os 
import requests
import json

def newton_formula():
  url = "https://newton.vercel.app/api/v2/factor/x%5E2-1"
  api_request = requests.get(url)
  data = json.loads(api_request.text)
  return data['file']
  
