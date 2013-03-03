#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings

#USE_ONLY_REGISTERED_USERS = getattr(settings, 'CONFIDENCE_CIRCLE_ONLY_REGISTERED_USERS', False)

SINGLETON = getattr(settings, 'CONFIDENCE_CIRCLE_ONLY_ONE', False)
EXPIRE_DAYS = getattr(settings, 'CONFIDENCE_CIRCLE_EXPIRE_DAYS', 7)
INVITE_BY_MAIL = getattr(settings, 'CONFIDENCE_CIRCLE_INVITE_BY_EMAIL', True)