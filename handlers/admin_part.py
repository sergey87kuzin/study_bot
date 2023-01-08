import os
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import bot
from db.work_with_db import (change_user_status, delete_file_from_db,
                             get_all_files, get_file_id, get_unanswered_users,
                             get_user_answers, save_file_to_db)
from keyboards.admin_keyboard import (admin_kb, answer_kb, file_action_kb,
                                      get_admin_to_user_kb, get_file_list,
                                      get_unanswered_users_kb, list_kb,
                                      people_kb, status_kb)
from src.helper import write_json
from src.questions import AdminButtons, Errors
from src.states import DataFSM, UserDataFSM, UserFSM


async def start_admin(message: types.Message):
    ''' react for /admin command. starts the admin cicle '''
    try:
        if str(message.from_user.id) in os.getenv('IDS'):
            await message.answer(
                text=AdminButtons.TEXT.value, reply_markup=admin_kb
            )
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await message.answer(
                text=Errors.ERROR.value
            )


''' file part '''


async def get_action(callback: types.CallbackQuery, state: FSMContext):
    ''' if admin chooses AUDIO/VIDEO, sends kb with action and
    saves it to state '''
    try:
        await callback.message.answer(
            text=AdminButtons.ACTION.value, reply_markup=file_action_kb
        )
        await DataFSM.data.set()
        async with state.proxy() as data:
            data['data'] = callback.data
        await DataFSM.next()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def get_descr(callback: types.CallbackQuery, state: FSMContext):
    ''' if admin choose ADD_AUDIO/ADD_VIDEO, asks to input description
    and saves it to state '''
    try:
        await callback.message.answer(
            text=AdminButtons.TEXT_ADD_DESCR.value
        )
        async with state.proxy() as data:
            data['action'] = callback.data
        await DataFSM.next()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def get_file(message: types.Message, state: FSMContext):
    ''' getting file and save it to state '''
    try:
        async with state.proxy() as data:
            data['description'] = message.text
        await DataFSM.next()
        await message.answer(
            text=AdminButtons.TEXT_ADD_FILE.value
        )
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def save_data(message: types.Message, state: FSMContext):
    ''' gets description and file from state and saves it to db '''
    try:
        async with state.proxy() as data:
            object_id = getattr(message, data['data']).file_id
            await save_file_to_db(data['data'], object_id, data['description'])
        await state.finish()
        await message.reply(text='OK')
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def show_all_files(callback: types.CallbackQuery, state: FSMContext):
    ''' sends to admin all files with description '''
    try:
        async with state.proxy() as data:
            file_type = data['data']
        files = get_all_files(file_type)
        if file_type == 'voice':
            for f in files:
                await bot.send_voice(
                    callback.from_user.id, caption=f['descr'], voice=f['id']
                )
        elif file_type == 'video_note':
            for f in files:
                await bot.send_video_note(
                    callback.from_user.id, caption=f['descr'],
                    video_note=f['id']
                )
        await state.finish()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def choose_file_to_del(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['action'] = callback.data
            await callback.message.answer(
                text=AdminButtons.CHOOSE_FILE.value,
                reply_markup=get_file_list(data['data'])
            )
        await DataFSM.next()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def delete_file(callback: types.CallbackQuery, state: FSMContext):
    ''' deletes file '''
    try:
        async with state.proxy() as data:
            delete_file_from_db(data['data'], callback.data)
        await state.finish()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer(text='OK')


''' start of people part '''


async def work_with_people(callback: types.CallbackQuery, state: FSMContext):
    ''' if admin chooses people button '''
    try:
        if str(callback.from_user.id) in os.getenv('IDS'):
            await UserDataFSM.action.set()
            await callback.message.reply(
                AdminButtons.PEOPLE.value,
                reply_markup=people_kb
            )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def answer_part(callback: types.CallbackQuery, state: FSMContext):
    ''' answer part of work-with-people admin way '''
    try:
        if str(callback.from_user.id) in os.getenv('IDS'):
            async with state.proxy() as data:
                data['action'] = callback.data
            await UserDataFSM.next()
            await callback.message.reply(
                AdminButtons.CHOOSE_LESSON.value,
                reply_markup=answer_kb
            )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def list_part(callback: types.CallbackQuery, state: FSMContext):
    ''' list part of work-with-people admin way '''
    try:
        if str(callback.from_user.id) in os.getenv('IDS'):
            async with state.proxy() as data:
                data['action'] = callback.data
            await UserDataFSM.next()
            await callback.message.reply(
                AdminButtons.CHOOSE_LESSON.value,
                reply_markup=list_kb
            )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def get_user_for_ans(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose user to answer '''
    try:
        if str(callback.from_user.id) in os.getenv('IDS'):
            async with state.proxy() as data:
                data['lesson'] = callback.data
            await UserDataFSM.next()
            await callback.message.reply(
                AdminButtons.CHOOSE_USER.value,
                reply_markup=get_unanswered_users_kb(callback.data[4:])
            )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def show_lesson_users(callback: types.CallbackQuery, state: FSMContext):
    ''' shows people who have no status == 3 '''
    try:
        if str(callback.from_user.id) in os.getenv('IDS'):
            users = get_unanswered_users(callback.data[5:])
            for user in users:
                await callback.message.reply(
                    f'<b style="color:blue !important">{user}</b>',
                    'HTML'
                )
            await state.finish()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def choose_answer(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose answer type '''
    try:
        async with state.proxy() as data:
            data['user'] = callback.data
            text = get_user_answers(data['lesson'][4:], callback.data)
            markup = get_admin_to_user_kb(data['lesson'][4:], callback.data)
        await state.finish()
        await UserFSM.lesson.set()
        await callback.message.answer(
            text=text, reply_markup=markup
        )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def choose_file(callback: types.CallbackQuery, state: FSMContext):
    ''' allows admin to choose file to send user '''
    try:
        await UserFSM.next()
        await UserFSM.next()
        ans_type, lesson, user = callback.data.split(', ')[:3]
        async with state.proxy() as data:
            data['lesson'] = lesson
            data['user'] = user
            data['ans_type'] = ans_type
        await UserFSM.next()
        if ans_type in ('send_new_voice', 'send_new_video_note'):
            await callback.message.answer(
                text=AdminButtons.WRITE_ANSW.value
            )
        else:
            await callback.message.answer(
                text=AdminButtons.CHOOSE_FILE.value,
                reply_markup=get_file_list(ans_type[5:])
            )
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer()


async def send_message_from_admin(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            if message.voice:
                await bot.send_voice(data['user'], voice=message.voice.file_id)
            elif message.video_note:
                await bot.send_video_note(
                    data['user'], video_note=message.video_note.file_id
                )
        await message.reply(
            text=AdminButtons.STATUS.value, reply_markup=status_kb)
        await UserFSM.next()
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def send_answer(callback: types.CallbackQuery, state: FSMContext):
    ''' sends message to user '''
    try:
        async with state.proxy() as data:
            if data['ans_type'] == 'send_voice':
                file_id = get_file_id('voice', callback.data)
                await bot.send_voice(data['user'], voice=file_id)
            elif data['ans_type'] == 'send_video_note':
                file_id = get_file_id('video_note', callback.data)
                await bot.send_video_note(data['user'], video_note=file_id)
            elif data['ans_type'] == 'send_mess':
                await bot.send_message(
                    data['user'], text=callback.message.text
                )
        await UserFSM.next()
        await callback.message.reply(
            text=AdminButtons.STATUS.value, reply_markup=status_kb)
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer(text='OK')


async def change_status(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            change_user_status(data['lesson'], data['user'], callback.data)
        await state.finish()
    except Exception as e:
        write_json(callback)
        logging.warning(e)
        await state.finish()
        await callback.message.answer(
            text=Errors.ERROR.value
        )
    await callback.answer(text='OK')


async def cancel_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in os.getenv('IDS'):
        current_state = await state.get_state()
        if not current_state:
            return
        await state.finish()
        await message.reply('OK')


''' register handlers of file and people parts '''


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
        get_action, Text(equals=['voice', 'video_note']), state=None
    )
    dp.register_callback_query_handler(
        get_descr, Text(equals=['add_file']),
        state=DataFSM.action
    )
    dp.register_callback_query_handler(
        show_all_files, Text(equals=['all_files']),
        state=DataFSM.action
    )
    dp.register_callback_query_handler(
        choose_file_to_del, Text(equals=['del_file']),
        state=DataFSM.action
    )
    dp.register_callback_query_handler(
        delete_file, state=DataFSM.description
    )
    dp.register_message_handler(
        get_file, state=DataFSM.description
    )
    dp.register_message_handler(
        save_data, content_types=['voice', 'video_note'], state=DataFSM.file_id
    )
    dp.register_callback_query_handler(
        work_with_people, Text(equals='answ'), state=None
    )
    dp.register_callback_query_handler(
        answer_part, Text(equals='answer'), state=UserDataFSM.action
    )
    dp.register_callback_query_handler(
        list_part, Text(equals='list'), state=UserDataFSM.action
    )
    dp.register_callback_query_handler(
        get_user_for_ans, Text(startswith='ans_'), state=UserDataFSM.lesson
    )
    dp.register_callback_query_handler(
        show_lesson_users, Text(startswith='list_'), state=UserDataFSM.lesson
    )
    dp.register_callback_query_handler(
        choose_answer, state=UserDataFSM.user
    )
    dp.register_callback_query_handler(
        choose_file, Text(startswith='send_'),
        state=UserFSM.lesson
    )
    dp.register_message_handler(
        send_message_from_admin, content_types=['voice', 'video_note'],
        state=UserFSM.file_id
    )
    dp.register_callback_query_handler(
        send_answer, state=UserFSM.file_id
    )
    dp.register_callback_query_handler(
        change_status, state=UserFSM.set_status
    )
