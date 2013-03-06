#!/usr/bin/env python
# encoding: utf-8

from slugify import slugify

from django.conf import settings
from django.db import models
from django.utils.translation import  ugettext_lazy as _
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.managers import QueryManager

import settings as app_settings

class ConfidenceCircle(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='in_confidencecircle_set', through='confidence_circle.ConfidenceCircleStatus', blank=True, null=True)

    class Meta:
        verbose_name = _('confidence circle')
        verbose_name_plural = _('confidence circles')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('confidence_circle_detail', kwargs={'slug':self.slug, 'confidencecircle_pk':self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ConfidenceCircle, self).save(*args, **kwargs)

    def add_user(self, user):
        self.users.add(user)

    def is_member(self, user):
        return True if user in self.users.auth() else False

if app_settings.SINGLETON:
    settings.AUTH_USER_MODEL.confidence_circle = property(lambda u: ConfidenceCircle.objects.get_or_create(user=u, name=_('your confidence circle')))


class ConfidenceCircleStatus(models.Model):
    STATUS = Choices(
                    (0, 'pending', _('authorization pending')),
                    (1, 'auth', _('currently authorized')),
                    (2, 'blocked', _('blocked')),
                    (3, 'rejected', _('invitation rejected')),
                    )

    circle = models.ForeignKey(ConfidenceCircle)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(choices=STATUS, default=STATUS.auth)

    objects = models.Manager()
    pending = QueryManager(status=STATUS.pending)
    auth = QueryManager(status=STATUS.auth)
    blocked = QueryManager(status=STATUS.blocked)

    class Meta:
        unique_together = ('user', 'circle')

    def __unicode__(self):
        return '%(user)s is %(status)s on %(circle)s' % {'user':self.user, 'status':self.get_status_display(), 'circle': self.circle}

"""
if app_settings.INVITE_BY_MAIL:

    class PendingAcceptanceManager(models.Manager):
        def generate_invitation(self, circle, email):
            pass


    class PendingAcceptance(models.Model):
        circle = models.ForeignKey(ConfidenceCircle)
        email = models.EmailField(_('e-mail'))
        key = models.CharField(_('invitation key'), max_length=40, unique=True)
        date_invited = models.DateTimeField(_('date invited'), auto_now_add=True)

"""