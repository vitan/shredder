#!/usr/bin/env python
#Added by Weitao Zhou <zhouwtlord@gmail.com> 

from django import forms
from django.conf import settings

from apps.questions.question.models import Question, Tag
import apps.questions.settings as question_settings

class ShareQuestionForm(forms.Form):

    description = forms.CharField(
        label=u"Question Description",
        max_length=question_settings.QUESTION_MAX_LENGTH,
        widget=forms.Textarea,
    )
    tag_list = forms.CharField(
        label=u"Tags",
        max_length=question_settings.FORM_TAG_LIST_MAX_LENGTH,
        required=False,
    )
    difficulty = forms.ChoiceField(
        label=u"Difficulty Level",
        choices=Question.QUESTION_DIFFICULTY,
    )
    estimated_time = forms.IntegerField(
        label=u"Estimated Time(By Minute)",
    )

    def clean_tag_list(self):
        data = self.cleaned_data['tag_list']
        return set(data.split(u','))


class TagAdminForm(forms.ModelForm):

    class Meta:
        model = Tag

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.strip()
