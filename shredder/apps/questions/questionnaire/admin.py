#! /usr/bin/env python
#Added by weitao zhou <zhouwtlord@gmail.com>

from django.contrib import admin

from apps.questions.questionnaire.models import Department, Position


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields  = ['name',]
    list_filter = ('name',)

admin.site.register(Department, DepartmentAdmin)


class PositionAdmin(admin.ModelAdmin):

    list_display = ('name',
                    'department',
                    'is_open',
                   )
    search_fields = ['name',
                    'department',
                    'is_open',]
    ordering = ['is_open',]
    list_filter = ('is_open',
                   'name',
                   'department',)

admin.site.register(Position, PositionAdmin)
