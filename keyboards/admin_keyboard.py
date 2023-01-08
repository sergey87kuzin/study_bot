import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.questions import AdminButtons
from src.literals import DBNAME


def create_kb(buttons):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard.add(InlineKeyboardButton(**button))
    return keyboard


ADMIN_KEYBOARD = ({'text': AdminButtons.AUDIO.value,
                   'callback_data': 'voice'},
                  {'text': AdminButtons.VIDEO.value,
                   'callback_data': 'video_note'},
                  {'text': AdminButtons.PEOPLE.value,
                   'callback_data': 'answ'})
ADMIN_TO_USER_KB = (
    {'text': AdminButtons.SEND_AUDIO.value,
     'callback_data': 'send_voice'},
    {'text': AdminButtons.SEND_NEW_AUDIO.value,
     'callback_data': 'send_new_voice'},
    {'text': AdminButtons.SEND_VIDEO.value,
     'callback_data': 'send_video_note'},
    {'text': AdminButtons.SEND_NEW_VIDEO.value,
     'callback_data': 'send_new_video_note'},
    {'text': AdminButtons.SEND_MESSAGE.value,
     'callback_data': 'send_mess'}
)
FILE_ACTION_KB = (
    {'text': AdminButtons.ADD.value,
     'callback_data': 'add_file'},
    {'text': AdminButtons.ALL.value,
     'callback_data': 'all_files'},
    {'text': AdminButtons.DEL.value,
     'callback_data': 'del_file'}
)
PEOPLE_KB = (
    {'text': AdminButtons.ANSWER.value,
     'callback_data': 'answer'},
    {'text': AdminButtons.LIST.value,
     'callback_data': 'list'}
)
ANSWER_KB = (
    {'text': AdminButtons.LESSON_1.value,
     'callback_data': 'ans_first'},
    {'text': AdminButtons.LESSON_2.value,
     'callback_data': 'ans_sec'},
    {'text': AdminButtons.LESSON_3.value,
     'callback_data': 'ans_third'},
    {'text': AdminButtons.FOR_ALL.value,
     'callback_data': 'ans_all'},
)
LIST_KB = (
    {'text': AdminButtons.LESSON_1.value,
     'callback_data': 'list_first'},
    {'text': AdminButtons.LESSON_2.value,
     'callback_data': 'list_sec'},
    {'text': AdminButtons.LESSON_3.value,
     'callback_data': 'list_third'}
)
STATUS_KB = (
    {'text': AdminButtons.OK.value,
     'callback_data': '3'},
    {'text': AdminButtons.NOT_OK.value,
     'callback_data': '2'}
)
admin_kb = create_kb(ADMIN_KEYBOARD)
admin_to_user_kb = create_kb(ADMIN_TO_USER_KB)
file_action_kb = create_kb(FILE_ACTION_KB)
people_kb = create_kb(PEOPLE_KB)
answer_kb = create_kb(ANSWER_KB)
list_kb = create_kb(LIST_KB)
status_kb = create_kb(STATUS_KB)


def get_unanswered_users_kb(lesson):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        users = cursor.execute(
            ('SELECT user_id, user_name FROM user_answers ' +
             f'WHERE {lesson}_status!=:ans'), {'ans': 3}
        ).fetchall()
        BUTTONS = [
            {'text': user[1], 'callback_data': user[0]}
            for user in users
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


def get_admin_to_user_kb(lesson, user):
    BUTTONS = []
    for but in ADMIN_TO_USER_KB:
        button = but.copy()
        button['callback_data'] = f'{but["callback_data"]}, {lesson}, {user}'
        BUTTONS.append(button)
    return create_kb(BUTTONS)
