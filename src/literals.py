from src.questions import FirstLesson, SecondLesson, ThirdLesson

DBNAME = 'bot.db'

ADD_ANSWERS_TO_USER = {'l1q1': 'first_les_first_quest',
                       'l1q2': 'first_les_sec_quest',
                       'l1q3': 'first_les_third_quest',
                       'l2q1': 'sec_les_first_quest',
                       'l2q2': 'sec_les_sec_quest',
                       'l2q3': 'sec_les_third_quest',
                       'l3q1': 'third_les_first_quest',
                       'l3q2': 'third_les_sec_quest',
                       'l3q3': 'third_les_third_quest'}
LESSON_NUMBER = {'sq1': FirstLesson, 'sq2': SecondLesson, 'sq3': ThirdLesson}
LESSON_TEXT = {'first': FirstLesson, 'sec': SecondLesson, 'third': ThirdLesson}
STATUSES = {
    0: 'смотрит', 1: 'ждет ответа', 2: 'ждет исправления', 3: 'ответил'
}
NEXT_LESSON = {
    'first': 'sec_status', 'sec': 'third_status', 'third': 'answered'
}
