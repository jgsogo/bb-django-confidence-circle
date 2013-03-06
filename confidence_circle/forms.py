#!/usr/bin/env python
# encoding: utf-8

from django import forms

from confidence_circle.models import ConfidenceCircle

class ConfidenceCircleForm(forms.ModelForm):

    class Meta:
        model = ConfidenceCircle

    def __init__(self, owner, *args, **kwargs):
        self.owner = owner
        super(ConfidenceCircleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ConfidenceCircleForm, self).save(commit=False)
        instance.user = self.owner
        instance.save()
        return instance