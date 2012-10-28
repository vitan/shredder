#!/usr/bin/env python
# Added by Weitao Zhou <zhouwtlord@gmail.com>

from django.db import models
from django.contrib.auth.models import User

from apps.common.models import Base
from apps.questions.question.models import Question, Tag


__all__ = [
    'Department', 'Position', 'Questionnaire',
]


class Department(Base):

    name = models.CharField(max_length=64, unique=True, db_index=True)

    def __str__(self):
        return u'Department - %s' % self.name
    __unicode__ = __str__


class Position(Base):

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return u'Position - %s' % self.name
    __unicode__ = __str__


class Questionnaire(Base):

    name = models.CharField(max_length=64, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    time_used = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    position = models.ManyToManyField(Position, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return u'Questionnaire - %s' % self.name
    __unicode__ = __str__

    def get_absolute_url(self):
        url = '/questionnaire/%s/' % self.pk
        return url

class QuestionnaireQuestion(Base):

    order = models.IntegerField(default=0)
    questionaire = models.ForeignKey(Questionnaire)
    question = models.ForeignKey(Question)
