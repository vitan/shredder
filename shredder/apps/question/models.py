#!/usr/bin/env python
# Added by Chaobin Tang <chaobin.py@gmail.com>
# Changed by Weitao Zhou <zhouwtlord@gmail.com>

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import truncate_words

from apps.common.models import Base
import settings as question_settings


__all__ = [
    'Tag', 'Question',
]


class Tag(Base):

    name = models.CharField(max_length=32, db_index=True)

    def __str__(self):
        return u'Tag - %s' % self.name
    __unicode__ = __str__


class Question(Base):

    QUESTION_DIFFICULTY = (
        (1, u'Basic'),
        (2, u'Intermediate'),
        (3, u'Experienced'),
        (4, u'Advanced'),
        (5, u'Expert')
    )
    DIFFICULTIES = dict(QUESTION_DIFFICULTY)

    description = models.CharField(max_length=question_settings.QUESTION_MAX_LENGTH)
    difficulty = models.IntegerField(
        choices=QUESTION_DIFFICULTY,
        default=3
    )
    estimated_time = models.IntegerField(u'Number of seconds needed to give the answer', default=60)
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_active = models.BooleanField(default=False)
    #FIXME weitao
    creator = models.ForeignKey(User)
    is_reviewed = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return u'Question - %s' % truncate_words(self.question, 5)
    __unicode__ = __str__

#    def get_answer_type(self):
#        try:
#            answer = self.answer
#        except (AttributeError, models.ObjectDoesNotExist):
#            answer = None
#        if answer:
#            return answer.get_answer_type()
#        else:
#            return u'Answer undefined.'

    def get_difficulty(self):
        return self.DIFFICULTIES.get(self.difficulty, 'unset')

''''
class Answer(Base):

    ANSWER_TYPE = (
        (1, 'open answer'),
        (2, 'one choice out of many'),
        (3, 'multi choice'),
        (4, 'true or false')
    )
    question = models.OneToOneField(Question)
    answer_type = models.IntegerField(choices=ANSWER_TYPE)
    text_answer = models.TextField(max_length=1000, blank=True, null=True)
    boolean_answer = models.BooleanField(default=True)

    def get_correct_answer(self):
        return

    def __str__(self):
        return u'Answer to Question[%s]' % unicode(self.question)
    __unicode__ = __str__

    def get_answer_type(self):
        return dict(self.ANSWER_TYPE).get(self.answer_type, u'Undefined type')
'''
