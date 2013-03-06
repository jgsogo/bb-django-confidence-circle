#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.sites.models import get_current_site

from organizations.backends import invitation_backend, registration_backend

from confidence_circle.models import ConfidenceCircle
from confidence_circle.forms import ConfidenceCircleForm, ConfidenceCircleUserAddForm, ConfidenceCircleUserForm
from confidence_circle.mixins import ConfidenceCircleMixin, ConfidenceCircleUserMixin

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
        kwargs.update({'request':self.request})
        return kwargs

    def get_success_url(self):
        return reverse("confidence_circle_home")

class ConfidenceCircleUpdate(ConfidenceCircleMixin, UpdateView):
    form_class = ConfidenceCircleForm

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleUpdate, self).get_form_kwargs()
        kwargs.update({'request':self.request})
        return kwargs


class ConfidenceCircleDelete(ConfidenceCircleMixin, DeleteView):

    def get_success_url(self):
        return reverse("confidence_circle_home")


# Views related to users

class ConfidenceCircleUserList(ConfidenceCircleMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.confidencecircle = self.get_confidencecircle()
        self.object_list = self.confidencecircle.users.all()
        context = self.get_context_data(object_list = self.object_list, confidencecircle_users = self.object_list, confidencecircle = self.confidencecircle)
        return self.render_to_response(context)

class ConfidenceCircleUserDetail(ConfidenceCircleUserMixin, DetailView):
    pass

class ConfidenceCircleUserCreate(ConfidenceCircleMixin, CreateView):
    form_class = ConfidenceCircleUserAddForm
    template_name = 'confidence_circle/confidencecircleuser_form.html'

    def get_success_url(self):
        return reverse('confidence_circle_user_list', kwargs={'confidencecircle_pk': self.confidencecircle.pk, 'slug':self.confidencecircle.slug})

    def get_form_kwargs(self):
        kwargs = super(ConfidenceCircleUserCreate, self).get_form_kwargs()
        kwargs.update({'confidence_circle': self.confidencecircle})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.confidencecircle = self.get_object()
        return super(ConfidenceCircleUserCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.confidencecircle = self.get_object()
        return super(ConfidenceCircleUserCreate, self).post(request, *args, **kwargs)

class ConfidenceCircleUserRemind(ConfidenceCircleUserMixin, DetailView):
    template_name = 'confidence_circle/confidencecircleuser_remind.html'

    def get_object(self, **kwargs):
        self.confidencecircle_user = super(ConfidenceCircleUserRemind, self).get_object()
        if self.confidencecircle_user.user.is_active:
            raise Http404(_("Already active"))
        return self.confidencecircle_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        invitation_backend().send_reminder(self.object.user,
            **{'domain': get_current_site(self.request),
               'confidencecircle': self.confidencecircle}
            )
        return redirect(self.object)

class ConfidenceCircleUserUpdate(ConfidenceCircleUserMixin, UpdateView):
    form_class = ConfidenceCircleUserForm

class ConfidenceCircleUserDelete(ConfidenceCircleUserMixin, DeleteView):
    def get_success_url(self):
        return reverse('confidence_circle_user_list', kwargs={'confidencecircle_pk': self.object.circle.pk, 'slug':self.object.circle.slug})

