import sqlite3
from src.questions import AdminButtons
from src.helper import create_kb
from src.literals import DBNAME


ADMIN_KEYBOARD = ({'text': AdminButtons.ADD_AUDIO.value,
                   'callback_data': 'voice'},
                  {'text': AdminButtons.ADD_VIDEO.value,
                   'callback_data': 'video_note'},
                  {'text': AdminButtons.ANSWER.value,
                   'callback_data': 'answ'})
ADMIN_TO_USER_KB = (
    {'text': AdminButtons.SEND_AUDIO.value,
     'callback_data': 'send_voice'},
    {'text': AdminButtons.SEND_VIDEO.value,
     'callback_data': 'send_video_note'},
    {'text': AdminButtons.SEND_MESSAGE.value,
     'callback_data': 'send_mess'}
)
admin_kb = create_kb(ADMIN_KEYBOARD)
admin_to_user_kb = create_kb(ADMIN_TO_USER_KB)


def get_unanswered_users_kb():
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        users = cursor.execute(
            'SELECT user_id, user_name FROM user_answers WHERE answered=:ans',
            {'ans': 1}
        ).fetchall()
        BUTTONS = [
            {'text': user[1], 'callback_data': user[0]} for user in users
        ]
        return create_kb(BUTTONS)


def get_file_list(file_type):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        files = cursor.execute(
            f'SELECT name, object_id FROM {file_type}'
        ).fetchall()
        BUTTONS = [
            {'text': file_[0], 'callback_data': file_[0]} for file_ in files
        ]
        return create_kb(BUTTONS)
