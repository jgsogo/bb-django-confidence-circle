#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import get_object_or_404
from confidence_circle.models import ConfidenceCircle, ConfidenceCircleStatus

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


class ConfidenceCircleUserMixin(ConfidenceCircleMixin):
    user_model = ConfidenceCircleStatus
    confidencecircle_user_context_name = 'confidencecircle_user'

    def get_user_model(self):
        return self.user_model

    def get_context_data(self, **kwargs):
        kwargs = super(ConfidenceCircleUserMixin, self).get_context_data(**kwargs)
        kwargs.update({self.confidencecircle_user_context_name: self.object, self.confidencecircle_context_name: self.object.circle})
        return kwargs

    def get_object(self):
        if hasattr(self, 'confidencecircle_user'):
            return self.confidencecircle_user
        confidencecircle_pk = self.kwargs.get('confidencecircle_pk', None)
        user_pk = self.kwargs.get('user_pk', None)
        self.confidencecircle_user = get_object_or_404(self.get_user_model().objects.select_related(), user__pk=user_pk, circle__pk=confidencecircle_pk)
        return self.confidencecircle_user
