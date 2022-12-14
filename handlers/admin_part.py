import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from db.work_with_db import save_file_to_db, get_file_id
from keyboards.admin_keyboard import (admin_kb, admin_to_user_kb,
                                      get_file_list, get_unanswered_users_kb)
from src.questions import AdminButtons
from src.helper import write_json


class UserFSM(StatesGroup):
    user = State()
    ans_type = State()
    file_id = State()


class DataFSM(StatesGroup):
    data = State()
    description = State()
    file_id = State()


async def start_admin(message: types.Message):
    ''' react for /admin command. starts the admin cicle '''
    write_json(message)
    if str(message.from_user.id) in os.getenv('IDS'):
        await message.answer(
            text=AdminButtons.TEXT.value, reply_markup=admin_kb
        )


async def get_descr(callback: types.CallbackQuery, state: FSMContext):
    ''' if admin choose ADD_AUDIO/ADD_VIDEO, asks to input description
    and saves it to state '''
    write_json(callback)
    await callback.message.answer(
        text=AdminButtons.TEXT_ADD_DESCR.value
    )
    await DataFSM.data.set()
    async with state.proxy() as data:
        data['data'] = callback.data
    await DataFSM.next()
    await callback.answer()


async def get_file(message: types.Message, state: FSMContext):
    ''' getting file and save it to state '''
    async with state.proxy() as data:
        data['description'] = message.text
    await DataFSM.next()
    await message.answer(
        text=AdminButtons.TEXT_ADD_FILE.value
    )


async def save_data(message: types.Message, state: FSMContext):
    ''' gets description and file from state and saves it to db '''
    async with state.proxy() as data:
        object_id = getattr(message, data['data']).file_id
        await save_file_to_db(data['data'], object_id, data['description'])
    await state.finish()
    await message.reply(text='OK')


async def get_user(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose user to answer '''
    if str(callback.from_user.id) in os.getenv('IDS'):
        await UserFSM.user.set()
        await callback.message.reply(
            AdminButtons.CHOOSE_USER.value,
            reply_markup=get_unanswered_users_kb()
        )
        await callback.answer()


async def choose_answer(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose answer type '''
    async with state.proxy() as data:
        data['user'] = callback.data
    await UserFSM.next()
    await callback.message.answer(
        text=AdminButtons.CHOOSE_ANSWER.value, reply_markup=admin_to_user_kb
    )
    await callback.answer()


async def choose_file(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose file to send user '''
    async with state.proxy() as data:
        data['ans_type'] = callback.data
    await UserFSM.next()
    if callback.data == 'send_mess':
        await callback.message.answer(
            text=AdminButtons.WRITE_ANSW.value
        )
    else:
        await callback.message.answer(
            text=AdminButtons.CHOOSE_FILE.value,
            reply_markup=get_file_list(callback.data[5:])
        )
    await callback.answer()


async def send_message_from_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(data['user'], text=message.text)
    await state.finish()


async def send_answer(callback: types.CallbackQuery, state: FSMContext):
    ''' sends message to user '''
    async with state.proxy() as data:
        if data['ans_type'] == 'send_voice':
            file_id = get_file_id('voice', callback.data)
            await bot.send_voice(data['user'], voice=file_id)
        elif data['ans_type'] == 'send_video_note':
            file_id = get_file_id('video_note', callback.data)
            await bot.send_video(data['user'], video=file_id)
        elif data['ans_type'] == 'send_mess':
            await bot.send_message(data['user'], text=callback.message.text)
    await state.finish()
    await callback.answer(text='OK')


async def cancel_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in os.getenv('IDS'):
        current_state = await state.get_state()
        if not current_state:
            return
        await state.finish()
        await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        cancel_handler, state='*', commands=['cancel']
    )
    dp.register_message_handler(
        cancel_handler, Text(equals='отмена', ignore_case=True), state='*'
    )
    dp.register_message_handler(
        start_admin, commands=['admin'], state=None
    )
    dp.register_callback_query_handler(
        get_descr, Text(equals=['voice', 'video_note']), state=None
    )
    dp.register_message_handler(
        get_file, state=DataFSM.description
    )
    dp.register_message_handler(
        save_data, content_types=['voice', 'video_note'], state=DataFSM.file_id
    )
    dp.register_callback_query_handler(
        get_user, Text(equals='answ'), state=None
    )
    dp.register_callback_query_handler(
        choose_answer, state=UserFSM.user
    )
    dp.register_callback_query_handler(
        choose_file, state=UserFSM.ans_type
    )
    dp.register_message_handler(send_message_from_admin, state=UserFSM.file_id)
    dp.register_callback_query_handler(
        send_answer, state=UserFSM.file_id
    )
    # dp.register_message_handler(
    #     get_answer_for_change_answer, state=FSMAdmin.answer
    # )
