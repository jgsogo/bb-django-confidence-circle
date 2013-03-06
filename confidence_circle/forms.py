#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.conf import settings

from organizations.backends import invitation_backend

from confidence_circle.models import ConfidenceCircle, ConfidenceCircleStatus

class ConfidenceCircleForm(forms.ModelForm):

    class Meta:
        model = ConfidenceCircle
        exclude = ('user', 'slug',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ConfidenceCircleForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ConfidenceCircleForm, self).save(commit=False)
        instance.user = self.request.user
        instance.save()
        return instance

class ConfidenceCircleUserAddForm(forms.ModelForm):
    email = forms.EmailField(max_length=75)

    class Meta:
        model = ConfidenceCircleStatus
        exclude = ('circle', 'user', 'status',)

    def __init__(self, request, confidencecircle, *args, **kwargs):
        self.request = request
        self.confidencecircle = confidencecircle
        super(ConfidenceCircleUserAddForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        The save method should create a new user in current ConfidenceCircle linking the User
        matching the provided email address. Of not matching User is found it should kick off the
        registration process. It needs to create a User in order to link it to the ConfidenceCircle
        """
        try:
            user = settings.AUTH_USER_MODEL.objects.get(email__iexact=self.cleaned_data['email'])
        except settings.AUTH_USER_MODEL.MultipleObjectsReturned:
            raise forms.ValidationError(_('This email address has been used multiple times.'))
        except settings.AUTH_USER_MODEL.DoesNotExist:
            user = invitation_backend().invite_by_mail(
                self.cleaned_data['email'],
                **{'domain': get_current_site(self.request),
                   'confidencecircle': self.confidencecircle}
                )
        return ConfidenceCircleStatus.objects.create(user=user, circle=self.confidencecircle)

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.confidencecircle.users.filter(email=email).exists():
            raise forms.ValidationError(_('There is already an user with this email address!'))

class ConfidenceCircleUserForm(forms.ModelForm):
    class Meta:
        model = ConfidenceCircleStatus
        exclude = ('user', 'circle',)