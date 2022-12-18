import os
from flask import Flask
from flask import request
import json
from create_bot import bot

app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_TOKEN')


@app.route('/', methods=['POST', 'GET'])
def some():
    if request.method == 'POST':
        resp = request.get_json()
        with open('answer.json', 'w') as f:
            json.dump(
                obj=resp, fp=f, ensure_ascii=False, indent=2,
                separators=(',', ': ')
            )
        with open('bot.txt', 'w') as f:
            f.write(', '.join(dir(bot)))
    return '<h1>Start my bot</h1>'


@app.route(f'/{TOKEN}', methods=['POST', 'GET'])
def index():
    print('message was here')
    return '<h1>Start my bot</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
