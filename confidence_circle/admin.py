#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin

from confidence_circle.models import ConfidenceCircle, ConfidenceCircleStatus

admin.site.register(ConfidenceCircle)
admin.site.register(ConfidenceCircleStatus)