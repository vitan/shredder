#!/usr/bin/env python
#Added by Weitao Zhou <zhouwtlord@gmail.com> 

from django import forms
from django.conf import settings

from apps.questions.question.models import Question, Tag
import apps.questions.settings as question_settings

class ShareQuestionForm(forms.Form):

    description = forms.CharField(
        label=u"Description",
        max_length=question_settings.QUESTION_MAX_LENGTH,
        widget=forms.Textarea,
    )
    tag_list = forms.CharField(
        label=u"Tags",
        max_length=question_settings.FORM_TAG_LIST_MAX_LENGTH,
        required=False,
    )
    difficulty = forms.ChoiceField(
        label=u"Difficulty-Level",
        choices=Question.QUESTION_DIFFICULTY,
    )
    estimated_time = forms.IntegerField(
        label=u"Estimated-Time(By Minute)",
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
        return {
            'description': self.cleaned_data['description'],
            'difficulty': self.cleaned_data['difficulty'],
            'estimated_time': self.cleaned_data['estimated_time'],
            'tag_obj_set':self.cleaned_data['tag_list'],
        }

#TODO (weizhou) abstract tag form as a common form in the future. And I should\
        #look Tag as an independent model, to put model Tag, TagAdminForm in common 
class TagAdminForm(forms.ModelForm):

    class Meta:
        model = Tag

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.strip()


class QuestionReviewForm(ShareQuestionForm):
    '''Base class is ShareQuestionForm.'''

    creator = forms.CharField(
        label=u"Creator",
    )
    date_updated = forms.DateTimeField(
        label=u"Last-Update",
    )
    status = forms.ChoiceField(
        label=u'Status',
        choices=Question.STATUS_NODE,
    )

    def get_cleaned_data(self):
        dict = super(QuestionReviewForm, self).get_cleaned_data()
        dict.update({
            'status': self.cleaned_data['status'],
        })
        return dict
