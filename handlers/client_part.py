import logging
import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from create_bot import bot
from db.work_with_db import (get_current_lesson, get_hello_video,
                             save_user_answer)
from src.helper import send_message_to_admin, write_json
from src.literals import LESSON_TEXT
from src.questions import Errors, FirstLesson, StartQuest
from src.states import AnswerFSM


async def start_of_dialog(message: types.Message, state: FSMContext):
    try:
        await AnswerFSM.lesson.set()
        await bot.send_video_note(
            message.from_user.id, video_note=get_hello_video()
        )
        time.sleep(10)
        await message.answer(
            text=StartQuest.HELLO.value
        )
        await message.answer(
            text=FirstLesson.LESSON_NAME.value
        )
        await message.answer(
            text=FirstLesson.FIRST_QUESTION.value
        )
        async with state.proxy() as data:
            data['lesson'] = 'first'
        await AnswerFSM.next()
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def first_answer(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['first_answer'] = message.text
            lesson = LESSON_TEXT[data['lesson']]
        await save_user_answer(
            message.from_user.id, message.from_user.full_name,
            data['lesson'], 'first', message.text
        )
        await AnswerFSM.next()
        await message.answer(text='thats ok')
        await message.answer(
            text=lesson.SECOND_QUESTION.value
        )
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def sec_answer(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['sec_answer'] = message.text
            lesson = LESSON_TEXT[data['lesson']]
        await save_user_answer(
            message.from_user.id, message.from_user.full_name,
            data['lesson'], 'sec', message.text
        )
        await AnswerFSM.next()
        await message.answer(
            text=lesson.THIRD_QUESTION.value
        )
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def third_answer(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['third_answer'] = message.text
            lesson_text = LESSON_TEXT[data['lesson']]
        await save_user_answer(
            message.from_user.id, message.from_user.full_name,
            data['lesson'], 'third', message.text
        )
        async with state.proxy() as data:
            lesson = data['lesson']
        await state.finish()
        user = message.from_user.id
        await send_message_to_admin(lesson, user)
        await message.answer(
            text=lesson_text.AFTER_QUESTION.value
        )
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


async def next_lesson(message: types.Message, state: FSMContext):
    try:
        lesson = get_current_lesson(message.from_user.id)
        await message.answer(text=LESSON_TEXT[lesson].FIRST_QUESTION.value)
        await AnswerFSM.lesson.set()
        async with state.proxy() as data:
            data['lesson'] = lesson
        await AnswerFSM.next()
    except Exception as e:
        write_json(message)
        logging.warning(e)
        await state.finish()
        await message.answer(
            text=Errors.ERROR.value
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        start_of_dialog, commands=['start', 'help'], state=None
    )
    dp.register_message_handler(
        first_answer, state=AnswerFSM.first_answer
    )
    dp.register_message_handler(
        sec_answer, state=AnswerFSM.sec_answer
    )
    dp.register_message_handler(
        third_answer, state=AnswerFSM.third_answer
    )
    dp.register_message_handler(
        next_lesson, commands=['next'], state=None
    )

# async def get_lesson_number(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data['lesson'] = callback.data
#     await AnswerFSM.next()
#     await callback.message.answer(
#         text=LESSON_NUMBER[callback.data].LESSON_NAME.value,
#         reply_markup=KEYBOARD[callback.data]
#     )
#     await callback.answer()


# async def get_user_question(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data['question'] = ADD_ANSWERS_TO_USER[callback.data]
#     await AnswerFSM.next()
#     await callback.message.answer(text='Ваш ответ:')
#     await callback.answer()


# async def get_user_answer(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['answer'] = message.text
#         await save_user_answer(
#             message.from_user.id, message.from_user.full_name,
#             data['question'], data['answer']
#         )
#     await AnswerFSM.next()
#     await message.answer(
#         text=AfterQuestion.TEXT.value,
#         reply_markup=client_keyboard.after_question_kb
#     )


# async def after_question(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data['after'] = callback.data
#     if callback.data == YES:
#         await state.finish()
#         await AnswerFSM.lesson.set()
#         await callback.message.answer(
#             text=StartQuest.QUESTION.value,
#             reply_markup=client_keyboard.start_kb
#         )
#     elif callback.data == NO:
#         await callback.message.answer(text='спасибо')
#         await state.finish()
#     elif callback.data == FINISH:
#         await callback.message.answer(text='спасибо')
#         async with state.proxy() as data:
#             await send_message_to_admin(
#                 data['question'], callback.from_user.id
#             )
#             await set_user_answered(callback.from_user.id)
#         await state.finish()


# async def answer(message: types.Message):
#     await message.answer(text=message.text)
#     await message.reply(text=message.text)
#     await bot.send_message(chat_id=message.from_user.id, text=message.text)


    # dp.register_message_handler(get_user_answer, state=AnswerFSM.answer)
    # dp.register_callback_query_handler(
    #     after_question, Text(equals=[YES, NO, FINISH]), state=AnswerFSM.after)
    # dp.register_message_handler(answer)
