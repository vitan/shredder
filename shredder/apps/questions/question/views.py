#!/usr/bin/env python
#Add by Weitao Zhou <zhouwtlord@gmail.com>

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from apps.common.views import AjaxResponseMixin
from apps.questions.question.models import Question, Tag
from apps.questions.question.forms import ShareQuestionForm, QuestionReviewForm
import apps.questions.settings as question_settings


__all__ = {
    'share_question',
    'question_list',
    'question_review',
}


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

    tag_cloud = Tag.objects.all()
    questions = Question.objects.all()
    paginator = Paginator(questions, question_settings.QUESTIONS_PER_PAGE)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        reports = paginator.page(page)
    except (EmptyPage, InvalidPage):
        reports = paginator.page(paginator.num_pages)

    pk_forms = dict()
    for report in reports.object_list:
        init = report.__dict__
        init['creator'] = report.creator
        init['tag_list'] = report.textual_tags
        form = QuestionReviewForm(initial=init)
        # TODO (weizhou) replace the pk with report's MD5 for security
        pk_forms[report.pk] = form

    return render_to_response(template_name, {
        'title': u"Question List",
        'reports': reports,
        'pk_forms': pk_forms,
        'tag_cloud': tag_cloud,
        },context_instance=RequestContext(request))


@login_required
def question_review(request, question_id):
    """Review the submitted question."""

    response = AjaxResponseMixin()
    if request.method == 'POST':
        form = QuestionReviewForm(request.POST)
        if form.is_valid():
            data = form.get_cleaned_data()
            question_obj = Question.objects.get(pk=question_id)
            question_obj.description = data['description']
            question_obj.estimated_time = data['estimated_time']
            question_obj.status = data['status']
            question_obj.difficulty = data['difficulty']

            question_obj.tags.clear()
            for tag_obj in data['tag_obj_set']:
                question_obj.tags.add(tag_obj)
            question_obj.save()

            return response.ajax_response()

        else:
            form_invalid = {'html': form.errors}
            return response.ajax_response(**form_invalid)
