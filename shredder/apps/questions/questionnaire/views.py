#!/usr/bin/env python
#Add by Weitao Zhou <zhouwtlord@gmail.com>

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from random import randint

from apps.common.views import AjaxResponseMixin
from apps.questions.questionnaire.models import Position, Questionnaire, QuestionnaireQuestion
from apps.questions.questionnaire.forms import GenerateQuestionnaireForm
from apps.questions.question.models import Tag, Question


__all__ = {
    'generate_questionnaire',
}


@login_required
def generate_questionnaire(request, template_name="questionnaire/generate-questionnaire.html"):
    '''Generate questionnaire as manually settings. '''

    response = AjaxResponseMixin()
    tag_cloud = Tag.objects.all()

    if request.method == 'POST':
        form = GenerateQuestionnaireForm(request.POST)
        if form.is_valid():
            kwargs = form.get_cleaned_data()

            if 'questionnaire_save' in request.POST:
                #TODO (weizhou) how to smartly deal with the foreignkey
                data = {
                    'name': kwargs['name'],
                    'description': kwargs['description'],
                    'time_used': kwargs['time_used'],
                }
                questionnaire_obj = Questionnaire(**data)
                questionnaire_obj.save()
                #TODO (weizhou) position field would be changed in the future
                questionnaire_obj.position.add(kwargs['position'])
                for tag_obj in kwargs['tag_obj_set']:
                    questionnaire_obj.tags.add(tag_obj)

                count = 0
                for pk in kwargs['question_order']:
                    map_obj = QuestionnaireQuestion(
                        questionnaire=questionnaire_obj,
                        question=Question.objects.get(pk=pk),
                        order=count
                    )
                    map_obj.save()
                    count += 1

            else:
                questions = auto_generate(**kwargs)
                items = [{
                    'pk': question.pk,
                    'desc': question.description,
                }
                    for question in questions
                ]
                data = {'items': items}
                return response.ajax_response(**data)
        else:
            #TODO (weizhou) form errors ajax transport
            pass

    return render_to_response(template_name, {
        'title': u"Generate Questionnaire",
        'form': GenerateQuestionnaireForm(),
        'tag_cloud': tag_cloud,
        }, context_instance=RequestContext(request))

def auto_generate(**kwargs):
    '''Generate a question list based on the given tags and level.'''

    question_objs = Question.objects.filter(status=3, tags__in=kwargs['tag_obj_set'])

    result = []
    for key, value in kwargs.iteritems():
        if key[:6] == "level_":
            diff_level_objs = question_objs.filter(difficulty=int(key[6:])).distinct()
            max = diff_level_objs.count()
            indexs = randint_n_generator(0, max, value)
            result.extend([diff_level_objs[i] for i in indexs])
    return result

def randint_n_generator(min, max, n):
    '''Return an int list containing 'n' random int numbers between min and max.'''
    
    result = set()
    while(True):
        num = randint(min, max-1)
        result.add(num)
        if len(result) == n:
            return result
