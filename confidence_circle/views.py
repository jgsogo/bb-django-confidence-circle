#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse

from confidence_circle.models import ConfidenceCircle
from confidence_circle.forms import ConfidenceCircleForm
from confidence_circle.mixins import ConfidenceCircleMixin

# Views about ConfidenceCircle model

class ConfidenceCircleList(ListView):
    def get_queryset(self):
        return ConfidenceCircle.objects.filter(user=self.request.user)


class ConfidenceCircleDetail(ConfidenceCircleMixin, DetailView):
    pass

class ConfidenceCircleCreate(CreateView):
    model = ConfidenceCircle
    form_class = ConfidenceCircleForm

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleCreate, self).get_form_kwargs()
        kwargs.update({'owner':self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("confidence_circle_home")

class ConfidenceCircleUpdate(ConfidenceCircleMixin, UpdateView):
    form_class = ConfidenceCircleForm

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleUpdate, self).get_form_kwargs()
        kwargs.update({'owner':self.request.user})
        return kwargs


class ConfidenceCircleDelete(ConfidenceCircleMixin, DeleteView):

    def get_success_url(self):
        return reverse("confidence_circle_home")

# Views related to users

class ConfidenceCircleUserList(ConfidenceCircleMixin, ListView):
    def get(self, request, *args, **kwargs):
        pass