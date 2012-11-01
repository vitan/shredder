#! /usr/bin/env python
#Added by weitao zhou <zhouwtlord@gmail.com>

from django.contrib import admin

from apps.questions.question.models import Tag
from apps.questions.question.forms import TagAdminForm


class TagAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields  = ['name',]
    ordering = ['name',]
    form = TagAdminForm

admin.site.register(Tag, TagAdmin)
