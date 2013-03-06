#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse

from confidence_circle.models import ConfidenceCircle
from confidence_circle.forms import ConfidenceCircleForm

class ConfidenceCircleList(ListView):
    model = ConfidenceCircle

    def get_queryset(self):
        return super(ConfidenceCircleList, self).get_queryset().filter(user=self.request.user)

class ConfidenceCircleDetail(DetailView):
    model = ConfidenceCircle

class ConfidenceCircleCreate(CreateView):
    model = ConfidenceCircle
    form_class = ConfidenceCircleForm

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleCreate, self).get_form_kwargs()
        kwargs.update({'owner':self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("confidence_circle_home")

class ConfidenceCircleUpdate(UpdateView):
    model = ConfidenceCircle
    form_class = ConfidenceCircleForm

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleUpdate, self).get_form_kwargs()
        kwargs.update({'owner':self.request.user})
        return kwargs


class ConfidenceCircleDelete(DeleteView):
    model = ConfidenceCircle

    def get_success_url(self):
        return reverse("confidence_circle_home")