import json
import os
import requests

from dotenv import load_dotenv
from flask import Flask, Response, request

load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def some():
    answer = ''
    if request.method == 'GET':
        print(request.__dict__)
        hub_challenge = request.url.split('&')[1]
        answer = hub_challenge.split('=')[1]
    if request.method == 'POST':
        resp = request.get_json()
        with open('answer.json', 'w') as f:
            json.dump(
                obj=resp, fp=f, ensure_ascii=False, indent=2,
                separators=(',', ': ')
            )
        text = resp['entry'][0]['messaging'][0]['message']['text']
        sender = resp['entry'][0]['messaging'][0]['sender']['id']
        recipient = resp['entry'][0]['messaging'][0]['recipient']['id']
        # text = resp['value']['message']['text']
        # sender = resp['value']['sender']['id']
        # recipient = resp['value']['recipient']['id']
        print(text, sender, recipient)
        if 'попытка' in text:
            send_message_to_insta(sender)
    return Response(answer, status=200)


def send_message_to_insta(sender_psid):
    print('was here')
    URL = 'https://graph.facebook.com/v15.0/me/messages'
    qs = {'access_token': os.getenv("INSTA_TOKEN"),
          'Authorization': f'Bearer {os.getenv("LONG_TERM_TOKEN")}'}
    request_body = {'recipient': {'id': sender_psid},
                    'message': {'text': 'success!'}}
    response = requests.post(
        url=URL, headers=qs, json=request_body
    )
    print('and here')
    print(response.__dict__)


if __name__ == '__main__':
    # app.run()
    app.run(host='localhost', debug=True, port=5001)
