from enum import Enum


class StartQuest(Enum):
    HELLO = 'Здравствуйте и прочее бла-бла-бла'
    VIDEO = 'Тут будет приветственное видео, а после него пауза'


class FirstLesson(Enum):
    LESSON_NAME = 'первый урок'
    FIRST_QUESTION = 'первый урок, первый вопрос'
    SECOND_QUESTION = 'первый урок, второй вопрос'
    THIRD_QUESTION = 'первый урок, третий вопрос'
    AFTER_QUESTION = 'спасибо за Ваши ответы'


class SecondLesson(Enum):
    LESSON_NAME = 'второй урок'
    FIRST_QUESTION = 'второй урок, первый вопрос'
    SECOND_QUESTION = 'второй урок, второй вопрос'
    THIRD_QUESTION = 'второй урок, третий вопрос'
    AFTER_QUESTION = 'спасибо за Ваши ответы'


class ThirdLesson(Enum):
    LESSON_NAME = 'третий урок'
    FIRST_QUESTION = 'третий урок, первый вопрос'
    SECOND_QUESTION = 'третий урок, второй вопрос'
    THIRD_QUESTION = 'третий урок, третий вопрос'
    AFTER_QUESTION = 'спасибо за Ваши ответы'


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
    ANSWER = 'ответить'
    CHOOSE_USER = 'выберите ученика'
    CHOOSE_ANSWER = 'как вы хотите ответить?'
    CHOOSE_FILE = 'выберите файл'
    SEND_AUDIO = 'отправить аудио'
    SEND_NEW_AUDIO = 'записать аудио'
    SEND_VIDEO = 'отправить видео'
    SEND_NEW_VIDEO = 'записать видео'
    SEND_MESSAGE = 'написать сообщение'
    WRITE_ANSW = 'введите ответ'
    AUDIO = 'Аудио'
    VIDEO = 'Видео'
    PEOPLE = 'Люди'
    ADD = 'записать'
    ALL = 'посмотреть все'
    DEL = 'удалить'
    LIST = 'списком'
    ACTION = 'Выберите действие'
    CHOOSE_LESSON = 'Выберите урок'
    LESSON_1 = 'урок 1'
    LESSON_2 = 'урок 2'
    LESSON_3 = 'урок 3'
    FOR_ALL = 'всем'
    STATUS = 'Как вам?'
    OK = 'Ok'
    NOT_OK = 'Переделывать'
    CHECK = 'отправить на проверку'


class Errors(Enum):
    ERROR = 'упс, что-то пошло не так('
