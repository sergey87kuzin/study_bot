from aiogram.dispatcher.filters.state import State, StatesGroup


class UserDataFSM(StatesGroup):
    action = State()
    lesson = State()
    user = State()


class UserFSM(StatesGroup):
    lesson = State()
    user = State()
    ans_type = State()
    file_id = State()
    set_status = State()


class DataFSM(StatesGroup):
    data = State()
    action = State()
    description = State()
    file_id = State()


class AnswerFSM(StatesGroup):
    lesson = State()
    first_answer = State()
    sec_answer = State()
    third_answer = State()
    after = State()
