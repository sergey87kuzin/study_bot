import sqlite3

from src.literals import DBNAME


def start_db():
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS user_answers(
            user_id text PRIMARY KEY, user_name text,
            first_les_first_quest text default 'no',
            first_les_sec_quest text default 'no',
            first_les_third_quest text default 'no',
            sec_les_first_quest text default 'no',
            sec_les_sec_quest text default 'no',
            sec_les_third_quest text default 'no',
            third_les_first_quest text default 'no',
            third_les_sec_quest text default 'no',
            third_les_third_quest text default 'no',
            answered integer default 0) '''
        )
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS video(
            name text PRIMARY KEY, object_id text)'''
        )
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS voice(
            name text PRIMARY KEY, object_id text)'''
        )


async def save_user_answer(user_id, user_name, field, answer):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        user = cursor.execute(
            'SELECT user_id FROM user_answers WHERE user_id=:user_id',
            {'user_id': user_id}
        ).fetchone()
        if not user:
            cursor.execute(
                f'INSERT INTO user_answers(user_id, user_name, {field})' +
                'VALUES(:user_id, :user_name, :answer)',
                {'user_id': user_id, 'user_name': user_name, 'answer': answer}
            )
            return
        cursor.execute(
            f'UPDATE user_answers SET {field}=:answer WHERE user_id=:user_id',
            {'answer': answer, 'user_id': user_id}
        )


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
            'UPDATE user_answers SET answerd=:res WHERE user_id=:user_id',
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
