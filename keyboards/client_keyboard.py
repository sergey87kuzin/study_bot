from src.helper import create_kb
from src.questions import (AfterQuestion, FirstLesson, SecondLesson,
                           StartQuest, ThirdLesson)
from src.literals import YES, NO, FINISH

START_KB = ({'text': StartQuest.FIRST_QUESTION.value,
             'callback_data': 'sq1'},
            {'text': StartQuest.SECOND_QUESTION.value,
             'callback_data': 'sq2'},
            {'text': StartQuest.THIRD_QUESTION.value,
             'callback_data': 'sq3'})
FIRST_QUESTION_KB = ({'text': FirstLesson.FIRST_QUESTION.value,
                      'callback_data': 'l1q1'},
                     {'text': FirstLesson.SECOND_QUESTION.value,
                      'callback_data': 'l1q2'},
                     {'text': FirstLesson.THIRD_QUESTION.value,
                      'callback_data': 'l1q3'})
SECOND_QUESTION_KB = ({'text': SecondLesson.FIRST_QUESTION.value,
                       'callback_data': 'l2q1'},
                      {'text': SecondLesson.SECOND_QUESTION.value,
                       'callback_data': 'l2q2'},
                      {'text': SecondLesson.THIRD_QUESTION.value,
                       'callback_data': 'l2q3'})
THIRD_QUESTION_KB = ({'text': ThirdLesson.FIRST_QUESTION.value,
                      'callback_data': 'l3q1'},
                     {'text': ThirdLesson.SECOND_QUESTION.value,
                      'callback_data': 'l3q2'},
                     {'text': ThirdLesson.THIRD_QUESTION.value,
                      'callback_data': 'l3q3'})
AFTER_QUESTION_KB = ({'text': AfterQuestion.YES.value,
                      'callback_data': YES},
                     {'text': AfterQuestion.NO.value,
                      'callback_data': NO},
                     {'text': AfterQuestion.FINISHED.value,
                      'callback_data': FINISH})


start_kb = create_kb(START_KB)
first_question_kb = create_kb(FIRST_QUESTION_KB)
second_question_kb = create_kb(SECOND_QUESTION_KB)
third_question_kb = create_kb(THIRD_QUESTION_KB)
after_question_kb = create_kb(AFTER_QUESTION_KB)
