#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import get_object_or_404
from confidence_circle.models import ConfidenceCircle

class ConfidenceCircleMixin(object):
    confidencecircle_model = ConfidenceCircle
    confidencecircle_context_name = 'confidencecircle'

    def get_confidencecircle_model(self):
        return self.confidencecircle_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.confidencecircle_context_name: self.get_confidencecircle()})
        return super(ConfidenceCircleMixin, self).get_context_data(**kwargs)

    def get_object(self):
        if hasattr(self, 'confidencecircle'):
            return self.confidencecircle
        confidencecircle_pk = self.kwargs.get('confidencecircle_pk', None)
        self.confidencecircle = get_object_or_404(self.get_confidencecircle_model(), pk=confidencecircle_pk)
        return self.confidencecircle
    get_confidencecircle = get_object # Now available when 'get_object' is overridden