import sqlite3

from src.literals import DBNAME, STATUSES, NEXT_LESSON


def start_db():
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS user_answers(
            user_id text PRIMARY KEY, user_name text,
            first_les_first_quest text default 'no',
            first_les_sec_quest text default 'no',
            first_les_third_quest text default 'no',
            first_status integer default 0,
            sec_les_first_quest text default 'no',
            sec_les_sec_quest text default 'no',
            sec_les_third_quest text default 'no',
            sec_status integer default 3,
            third_les_first_quest text default 'no',
            third_les_sec_quest text default 'no',
            third_les_third_quest text default 'no',
            third_status integer default 3,
            answered integer default 0) '''
        )
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS video_note(
            name text PRIMARY KEY, object_id text)'''
        )
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS voice(
            name text PRIMARY KEY, object_id text)'''
        )


async def save_user_answer(user_id, user_name, lesson, field, answer):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        user = cursor.execute(
            'SELECT user_id FROM user_answers WHERE user_id=:user_id',
            {'user_id': user_id}
        ).fetchone()
        if not user:
            cursor.execute(
                'INSERT INTO user_answers(user_id, user_name, ' +
                f'{lesson}_les_{field}_quest) ' +
                'VALUES(:user_id, :user_name, :answer)',
                {'user_id': user_id, 'user_name': user_name, 'answer': answer}
            )
            return
        cursor.execute(
            f'UPDATE user_answers SET {lesson}_les_{field}_quest=:answer ' +
            'WHERE user_id=:user_id', {'answer': answer, 'user_id': user_id}
        )
        conn.commit()


async def save_file_to_db(table, object_id, description):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO {table} (name, object_id) VALUES(:name, :object_id)',
            {'name': description, 'object_id': object_id}
        )


async def set_user_answered(user_id):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE user_answers SET answered=:res WHERE user_id=:user_id',
            {'res': 1, 'user_id': user_id}
        )


def get_file_id(table, name):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            f'SELECT object_id FROM {table} WHERE name=:name',
            {'name': name}
        ).fetchone()
        return result[0]


def get_all_files(table):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            f'SELECT name, object_id FROM {table}'
        ).fetchall()
        return ({'descr': name, 'id': object_id} for name, object_id in result)


def delete_file_from_db(table, name):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'DELETE FROM {table} WHERE name=:name',
            {'name': name}
        )


def get_unanswered_users(lesson):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            (f'SELECT user_name, {lesson}_status FROM user_answers WHERE ' +
             f'{lesson}_status!=:status'), {'status': 3}
        ).fetchall()
        return (f'{name} - {STATUSES[status]}' for name, status in result)


def change_user_status(lesson, user, status):
    next_les = NEXT_LESSON[lesson]
    if int(status) == 3:
        sql_str = (f'UPDATE user_answers SET {lesson}_status=:status, ' +
                   f'{next_les}=:zero WHERE user_id=:user_id')
    elif int(status) == 2:
        sql_str = (f'UPDATE user_answers SET {lesson}_status=:status ' +
                   'WHERE user_id=:user_id')
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            sql_str, {'status': int(status), 'zero': 0, 'user_id': user}
        )


def get_user_answers(lesson, user):
    sql_str = (f'SELECT {lesson}_les_first_quest, {lesson}_les_sec_quest,' +
               f' {lesson}_les_third_quest FROM user_answers' +
               ' WHERE user_id=:user')
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(sql_str, {'user': user}).fetchone()
    return ', '.join(result)


def get_current_lesson(user):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        statuses = cursor.execute(
            '''SELECT first_status, sec_status, third_status FROM
             user_answers WHERE user_id=:user''', {'user': user}
        ).fetchone()
        if statuses[0] != 3:
            return 'first'
        if statuses[1] != 3:
            return 'sec'
        return 'third'


def get_hello_video():
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        return cursor.execute(
            'SELECT object_id FROM video_note WHERE name=:name',
            {'name': 'приветствие'}
        ).fetchone()[0]
