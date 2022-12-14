import sqlite3
import json
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.literals import DBNAME, ADD_ANSWERS_TO_USER
from create_bot import bot


def create_kb(buttons):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard.add(InlineKeyboardButton(**button))
    return keyboard


async def send_message_to_admin(question, user_id):
    fields = [
        value for value in ADD_ANSWERS_TO_USER.values()
        if value.startswith(question[:3])
    ]
    fields = ', '.join(fields)
    sql_str = (
        f'SELECT user_name, {fields} FROM user_answers WHERE user_id=:user_id'
    )
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(sql_str, {'user_id': user_id}).fetchone()
        text = f'{result[0]} answerd: {", ".join(result[1:])}'
    await bot.send_message(os.getenv('ADMIN_ID'), text=text)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(
            obj=json.loads(data.as_json()), fp=f, ensure_ascii=False, indent=2,
            separators=(',', ': ')
        )


def write_to_file(data, filename='answer.txt'):
    attrs = [attr for attr in dir(data) if not attr.startswith('__')]
    with open(filename, 'w') as f:
        f.write(', '.join(attrs))
