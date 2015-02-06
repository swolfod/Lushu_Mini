__author__ = 'Swolfod'
# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns("WechatApi.views",
                       (r"^wechatSignature/$", "wechatSignature"),
                       (r"^authCallback/$", "authCallback"),
                       )