#!/usr/bin/env python
#Added by Weitao Zhou <zhouwtlord@gmail.com> 

from django import forms
from django.conf import settings

from apps.questions.questionnaire.models import Department, Position
from apps.questions.question.models import Tag, Question
import apps.questions.settings as form_settings


class PositionModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Position


class GenerateQuestionnaireForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(GenerateQuestionnaireForm, self).__init__(*args, **kwargs)
        for level in Question.QUESTION_DIFFICULTY:
            self.fields["level_%s" % level[0]] = forms.IntegerField(
                label=u"level %s" % level[1],
                min_value=0,
                max_value=Question.objects.filter(difficulty=level[0], status=3).count(),
                required=False,
            )

    #TODO (weizhou) should change the position as tag_list style
    position = forms.ModelChoiceField(
        label=u"Position",
        queryset=Position.objects.all().filter(is_open=True),
        empty_label=None,
    )
    tag_list = forms.CharField(
        label=u"Tags",
        max_length=form_settings.FORM_TAG_LIST_MAX_LENGTH,
        required=False,
    )
    name = forms.CharField(
        label=u"Name",
        max_length=form_settings.FORM_QUESTIONNAIRE_NAME_MAX_LENGTH,
    )
    description = forms.CharField(
        label=u"Description",
        max_length=form_settings.FORM_QUESTIONNAIRE_DESC_MAX_LENGTH,
        widget=forms.Textarea,
        required=False,
    )
    # TODO (weizhou) think about how to set time_used once have time
    time_used = forms.IntegerField(
        label=u"Time-used",
        min_value=0,
        required=False,
    )
    question_order = forms.CharField(
        max_length=255,
        required=False,
    )

    def clean_tag_list(self):
        '''Return a set containing Tag object.'''

        tag_obj_set = set()
        data = self.cleaned_data['tag_list']
        for tag in data.split(u','):
            if tag:
                try:
                    tag_obj = Tag.objects.get(name=tag.strip())
                    tag_obj_set.add(tag_obj)
                except Tag.DoesNotExist:
                    raise forms.ValidationError("Cannot find Tag %s" % tag)
        return tag_obj_set

    def clean_question_order(self):
        data = self.cleaned_data['question_order']
        return [pk for pk in data.split(u',') if pk]

    def get_cleaned_data(self):
        cleaned_dict = dict()
        cleaned_dict.update({
            'level_%s' % level[0]: self.cleaned_data['level_%s' % level[0]]
            for level in Question.QUESTION_DIFFICULTY if self.cleaned_data['level_%s' % level[0]]
        })
        cleaned_dict.update({
            'position': self.cleaned_data['position'],
            'tag_obj_set': self.cleaned_data['tag_list'],
            'name': self.cleaned_data['name'],
            'description': self.cleaned_data['description'],
            'question_order': self.cleaned_data['question_order'],
            'time_used': self.cleaned_data['time_used'],
        })

        return cleaned_dict
