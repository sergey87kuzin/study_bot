import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('INSTAGRAM_TOKEN')

URL = 'https://graph.facebook.com/v15.0/me'

data = {'access_token': TOKEN}

response = requests.get(URL, params=data).json()
with open('insta.json', 'w') as f:
    json.dump(
        obj=response, fp=f, ensure_ascii=False, indent=2,
        separators=(',', ': ')
    )
