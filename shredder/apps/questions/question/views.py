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
    """
    display the share question form
    """
    if request.method == 'POST':
        form  = ShareQuestionForm(request.POST)
        if form.is_valid():
            des = form.cleaned_data['description']
            dif = form.cleaned_data['difficulty']
            est = form.cleaned_data['estimated_time']
            tag_list = form.cleaned_data['tag_list']

            question_object = Question(
                description=des,
                difficulty=dif,
                estimated_time=est,
                creator=request.user)
            question_object.save()
            # TODO (weitao zhou)bulk insert optimization 
            for tag in tag_list:
                tag_object, created = Tag.objects.get_or_create(name=tag)
                question_object.tags.add(tag_object)

        else:
            return render_to_response(template_name, {
                'title': u"Share My Question",
                'form': form,
                }, context_instance=RequestContext(request))

    return render_to_response(template_name, {
        'title': u"Share My Question",
        'form': ShareQuestionForm(),
        },context_instance=RequestContext(request))


@login_required
def question_list(request, template_name='question/question-list.html'):
    """
    list the submitted questions
    """
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
