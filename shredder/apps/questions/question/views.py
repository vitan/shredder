#!/usr/bin/env python
#Add by Weitao Zhou <zhouwtlord@gmail.com>

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.questions.question.forms import ShareQuestionForm
from apps.questions.question.models import Question, Tag


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
        'form': ShareQuestionForm(), },
        context_instance=RequestContext(request))