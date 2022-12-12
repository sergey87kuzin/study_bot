from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.work_with_db import save_user_answer, set_user_answered
from keyboards import client_keyboard
from src.literals import ADD_ANSWERS_TO_USER, FINISH, LESSON_NUMBER, NO, YES
from src.questions import AfterQuestion, StartQuest
from src.helper import send_message_to_admin

KEYBOARD = {'sq1': client_keyboard.first_question_kb,
            'sq2': client_keyboard.second_question_kb,
            'sq3': client_keyboard.third_question_kb}


class AnswerFSM(StatesGroup):
    lesson = State()
    question = State()
    answer = State()
    after = State()


async def start_of_dialog(message: types.Message):
    await AnswerFSM.lesson.set()
    await message.answer(
        text=StartQuest.QUESTION.value,
        reply_markup=client_keyboard.start_kb
    )


async def get_lesson_number(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['lesson'] = callback.data
    await AnswerFSM.next()
    await callback.message.answer(
        text=LESSON_NUMBER[callback.data].LESSON_NAME.value,
        reply_markup=KEYBOARD[callback.data]
    )
    await callback.answer()


async def get_user_question(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = ADD_ANSWERS_TO_USER[callback.data]
    await AnswerFSM.next()
    await callback.message.answer(text='Ваш ответ:')
    await callback.answer()


async def get_user_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
        await save_user_answer(
            message.from_user.id, message.from_user.full_name,
            data['question'], data['answer']
        )
    await AnswerFSM.next()
    await message.answer(
        text=AfterQuestion.TEXT.value,
        reply_markup=client_keyboard.after_question_kb
    )


async def after_question(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['after'] = callback.data
    if callback.data == YES:
        await state.finish()
        await callback.message.answer(
            text=StartQuest.QUESTION.value,
            reply_markup=client_keyboard.start_kb
        )
    elif callback.data == NO:
        await callback.message.answer(text='спасибо')
        await state.finish()
    elif callback.data == FINISH:
        await callback.message.answer(text='спасибо')
        async with state.proxy() as data:
            await send_message_to_admin(
                data['question'], callback.from_user.id
            )
            await set_user_answered(callback.from_user.id)
        await state.finish()


# async def answer(message: types.Message):
#     await message.answer(text=message.text)
#     await message.reply(text=message.text)
#     await bot.send_message(chat_id=message.from_user.id, text=message.text)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        start_of_dialog, commands=['start', 'help'], state=None
    )
    dp.register_callback_query_handler(
        get_lesson_number, Text(equals=LESSON_NUMBER.keys()),
        state=AnswerFSM.lesson
    )
    dp.register_callback_query_handler(
        get_user_question, Text(equals=ADD_ANSWERS_TO_USER.keys()),
        state=AnswerFSM.question
    )
    dp.register_message_handler(get_user_answer, state=AnswerFSM.answer)
    dp.register_callback_query_handler(
        after_question, Text(equals=[YES, NO, FINISH]), state=AnswerFSM.after)
