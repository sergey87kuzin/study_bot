import sqlite3
import json
import os
from keyboards.admin_keyboard import get_admin_to_user_kb
from src.literals import DBNAME, ADD_ANSWERS_TO_USER
from src.states import UserFSM
from create_bot import bot


async def send_message_to_admin(question, user_id):
    fields = [
        value for value in ADD_ANSWERS_TO_USER.values()
        if value.startswith(question[:3])
    ]
    fields = ', '.join(fields)
    sql_str = (
        f'SELECT user_name, {fields} FROM user_answers WHERE user_id=:user_id'
    )
    await UserFSM.lesson.set()
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(sql_str, {'user_id': user_id}).fetchone()
        text = f'{result[0]} answerd: {", ".join(result[1:])}'
    await bot.send_message(
        os.getenv('ADMIN_ID'), text=text,
        reply_markup=get_admin_to_user_kb(question, user_id)
    )


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
