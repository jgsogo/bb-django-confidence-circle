#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from confidence_circle.models import ConfidenceCircle

class ConfidenceCircleList(ListView):
    model = ConfidenceCircle

    """
    def get_queryset(self):
        return super(ConfidenceCircleList, self).get_queryset()
    """

class ConfidenceCircleDetail(DetailView):
    model = ConfidenceCircle

class ConfidenceCircleCreate(CreateView):
    model = ConfidenceCircle

class ConfidenceCircleUpdate(UpdateView):
    model = ConfidenceCircle

class ConfidenceCircleDelete(DeleteView):
    model = ConfidenceCircle