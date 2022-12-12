from enum import Enum


class StartQuest(Enum):
    QUESTION = 'к какому уроку хотите оставить ответы?'
    FIRST_QUESTION = 'первый'
    SECOND_QUESTION = 'второй'
    THIRD_QUESTION = 'третий'


class FirstLesson(Enum):
    LESSON_NAME = 'первый урок'
    FIRST_QUESTION = 'первый урок, первый вопрос'
    SECOND_QUESTION = 'первый урок, второй вопрос'
    THIRD_QUESTION = 'первый урок, третий вопрос'


class SecondLesson(Enum):
    LESSON_NAME = 'второй урок'
    FIRST_QUESTION = 'второй урок, первый вопрос'
    SECOND_QUESTION = 'второй урок, второй вопрос'
    THIRD_QUESTION = 'второй урок, третий вопрос'


class ThirdLesson(Enum):
    LESSON_NAME = 'третий урок'
    FIRST_QUESTION = 'третий урок, первый вопрос'
    SECOND_QUESTION = 'третий урок, второй вопрос'
    THIRD_QUESTION = 'третий урок, третий вопрос'


class AfterQuestion(Enum):
    TEXT = 'хотите ли Вы ответить еще на один вопрос?'
    YES = 'Да'
    NO = 'Нет'
    FINISHED = 'Я закончил урок'


class AdminButtons(Enum):
    TEXT = 'чего изволите?'
    TEXT_ADD_DESCR = 'введите описание файла'
    TEXT_ADD_FILE = 'добавьте файл'
    ADD_AUDIO = 'добавить аудио'
    ADD_VIDEO = 'добавить видео'
    ANSWER = 'ответить ученику'
    CHOOSE_USER = 'выберите ученика'
    CHOOSE_ANSWER = 'как вы хотите ответить?'
    CHOOSE_FILE = 'выберите файл'
    SEND_AUDIO = 'отправить аудио'
    SEND_VIDEO = 'отправить видео'
    SEND_MESSAGE = 'написать сообщение'
