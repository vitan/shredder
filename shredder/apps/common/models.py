#!/usr/bin/env python
# Added by Chaobin Tang <chaobin.py@gmail.com>


from django.db import models


class Base(models.Model):

    class Meta:
        abstract = True
