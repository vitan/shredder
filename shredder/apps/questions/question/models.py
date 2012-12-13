#!/usr/bin/env python
# Added by Chaobin Tang <chaobin.py@gmail.com>, Weitao Zhou <zhouwtlord@gmail.com>

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.text import truncate_words

from apps.common.models import Base
import apps.questions.settings as question_settings


__all__ = [
    'Tag', 'Question', 'Candidate',
]


class Tag(Base):

    name = models.CharField(max_length=32, db_index=True, unique=True)

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

    STATUS_NODE = (
        (1, u'Submitted'),
        (2, u'Reviewed'),
        (3, u'Actived')
    )
    STATUS = dict(STATUS_NODE)

    QUESTION_TYPE = (
        (1, u'Subjective'),
        (2, u'Objective'),
    )
    TYPE = dict(QUESTION_TYPE)

    description = models.CharField(max_length=question_settings.QUESTION_MAX_LENGTH)
    difficulty = models.IntegerField(
        choices=QUESTION_DIFFICULTY,
        default=3
    )
    status = models.IntegerField(
        choices=STATUS_NODE,
        default=1
    )
    type = models.IntegerField(
        choices=QUESTION_TYPE,
        default=1
    )
    estimated_time = models.IntegerField(u'Number of minutes needed to give the answer', default=60)
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    # TODO (weitao zhou) the creators must be the login user? 
    creator = models.ForeignKey(User)

    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return u'Question - %s' % truncate_words(self.description, 5)
    __unicode__ = __str__

    def _get_textual_tags(self):
        text = [tag.name for tag in self.tags.all()]
        return u','.join(text)
    textual_tags = property(_get_textual_tags)


class ChoiceManager(models.Manager):
    
    def answer(self, keyword):
        """Return a list containing the candidates which are/is the answer of question."""

        return self.filter(question=keyword).filter(is_answer=True)


class Choice(Base):
    """Because we can look the subjective question as an objective question

    which only has one choice, the subjective question is generalized as an
    objective question. The field is_answer tags if the choice is answer."""

    description = models.CharField(
        verbose_name="Choice-Answer",
        max_length=question_settings.QUESTION_MAX_LENGTH,
    )
    question = models.ForeignKey(Question)
    is_answer = models.BooleanField(default=False)
    
    objects = ChoiceManager()

    def __str__(self):
        return u'Choice - %s' % truncate_words(self.description, 5)
    __unicode__ = __str__
