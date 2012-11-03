#!/usr/bin/env python
#Add by Weitao Zhou <zhouwtlord@gmail.com>

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.questions.question.forms import ShareQuestionForm
from apps.questions.question.models import Question, Tag
import apps.questions.settings as question_settings


@login_required
def share_question(request, template_name='question/share-question.html'):
    """Display the share question form."""

    tag_cloud = Tag.objects.all()
    if request.method == 'POST':
        form  = ShareQuestionForm(request.POST)
        if form.is_valid():
            data = form.get_cleaned_data()
            data['creator'] = request.user
            tag_obj_set = data.pop('tag_obj_set')
            question_object = Question(**data)
            question_object.save()
            #TODO (weizhou) need a good solution for save manytomanyfield
            for tag_obj in tag_obj_set:
                question_object.tags.add(tag_obj)
        else:
            return render_to_response(template_name, {
                'title': u"Share My Question",
                'form': form,
                'tag_cloud': tag_cloud,
                }, context_instance=RequestContext(request))

    return render_to_response(template_name, {
        'title': u"Share My Question",
        'form': ShareQuestionForm(),
        'tag_cloud': tag_cloud,
        },context_instance=RequestContext(request))


@login_required
def question_list(request, template_name='question/question-list.html'):
    """List the submitted questions."""

    questions = Question.objects.all()
    if request.method == 'POST':
        pass

    paginator = Paginator(questions, question_settings.QUESTIONS_PER_PAGE)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        reports = paginator.page(page)
    except (EmptyPage, InvalidPage):
        reports = paginator.page(paginator.num_pages)
    return render_to_response(template_name, {
        'title': u"Question List",
        'reports': reports,
        },context_instance=RequestContext(request))
