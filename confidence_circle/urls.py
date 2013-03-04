#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import settings as app_settings

from confidence_circle.views import (ConfidenceCircleDetail, ConfidenceCircleUpdate)
""",
                                     ConfidenceCircleUserList, ConfidenceCircleUserCreate,
                                     ConfidenceCircleUserRemind, ConfidenceCircleUserDetail,
                                     ConfidenceCircleUserUpdate, ConfidenceCircleUserBlock,
                                     ConfidenceCircleUserLeave)"""

# Create URL optional parameters
def get_url_optional():
    if app_settings.SINGLETON:
        return '(?:(?P<slug>[\w]+)/)?(?:(?P<pk>[\d]+)/)?'
    else:
        return '(?P<slug>[\w]+)/(?P<pk>[\d]+)/'
_url_optional = get_url_optional()


urlpatterns = patterns('',
    # Confidence circle urls
    url(r'^%s$' % _url_optional, login_required(ConfidenceCircleDetail.as_view()), name='confidence_circle_detail'),
    url(r'^' + _url_optional + 'edit/$', login_required(ConfidenceCircleUpdate.as_view()), name='confidence_circle_update'),

    # Confidence circle users urls
    #url(r'^' + _url_optional + 'people/$', login_required(ConfidenceCircleUserList.as_view()), name='confidence_circle_user_list'),
    #url(r'^' + _url_optional + 'people/add/$', login_required(ConfidenceCircleUserCreate.as_view()), name='confidence_circle_user_add'),
    #url(r'^' + _url_optional + 'people/(?P<pk>[\d]+)/remind/$', login_required(ConfidenceCircleUserRemind.as_view()), name='confidence_circle_user_remind'),
    #url(r'^' + _url_optional + 'people/(?P<pk>[\d]+)/$', login_required(ConfidenceCircleUserDetail.as_view()), name='confidence_circle_user_detail'),
    #url(r'^' + _url_optional + 'people/(?P<pk>[\d]+)/edit/$', login_required(ConfidenceCircleUserUpdate.as_view()), name='confidence_circle_user_edit'),
    #url(r'^' + _url_optional + 'people/(?P<pk>[\d]+)/block/$', login_required(ConfidenceCircleUserBlock.as_view()), name='confidence_circle_user_block'),
    #url(r'^' + _url_optional + 'leave/$', login_required(ConfidenceCircleUserLeave.as_view()), name='confidence_circle_user_leave'),
    )

if not app_settings.SINGLETON:
    from confidence_circle.views import ConfidenceCircleList, ConfidenceCircleCreate, ConfidenceCircleDelete
    urlpatterns += patterns('',
        url(r'^$', login_required(ConfidenceCircleList.as_view()), name='confidence_circle_list'),
        url(r'^add/$', login_required(ConfidenceCircleCreate.as_view()), name='confidence_circle_add'),
        url(r'^(?P<slug>[\w]+)/(?P<pk>[\d]+)/delete/$', login_required(ConfidenceCircleDelete.as_view()), name='confidence_circle_delete'),
        )
