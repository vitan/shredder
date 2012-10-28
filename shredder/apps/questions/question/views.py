#! /usr/bin/env python
#Added by Weitao Zhou <zhouwtlord@gmail.com>

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext

from apps.questions.question.models import Question, Tag


def share_question(request, template_name=''):
    """
    display the share question form
    """
    pass
