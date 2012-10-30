#!/usr/bin/env python
#Added by Weitao Zhou <zhouwtlord@gmail.com> 

from django import forms
from django.conf import settings

from apps.questions.questionnaire.models import Department, Position
from apps.questions.question.models import Tag, Question
import apps.questions.settings as form_settings


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

    def get_cleaned_data(self):
        cleaned_dict = dict()
        cleaned_dict.update({
            'level_%s' % level[0]: self.cleaned_data['level_%s' % level[0]]
            for level in Question.QUESTION_DIFFICULTY if self.cleaned_data['level_%s' % level[0]]
        })
        cleaned_dict.update({
            'position': self.cleaned_data['position'],
            'tag_obj_set': self.cleaned_data['tag_list'],
        })

        return cleaned_dict


"""
def questionnaire_form_factory(question=Question): 
    '''
    Return a form class GenerateQuestionnaire, expect model Question to
    init the dynamic form field.
    '''

    fields = {
        'position': forms.ModelChoiceField(
            label=u"Position",
            queryset=Position.objects.all().filter(is_open=True),
            empty_label=None,
        ),
        'tags': forms.ModelChoiceField(
            label=u"Generate from Tags",
            widget=forms.CheckboxSelectMultiple,
            queryset=Tag.objects.all(),
            empty_label=None,
        ),
    }

    for level in question.QUESTION_DIFFICULTY:
        fields["level_%s" % level[0]] = forms.IntegerField(
            label=u"level %s" % level[1],
            min_value=0,
            max_value=question.objects.filter(difficulty=level[0]).count(),
            required=False,
        )

    return type('GenerateQuestionnaire', (forms.BaseForm,), {'base_fields': fields })


GenerateQuestionnaireForm = questionnaire_form_factory()
"""
