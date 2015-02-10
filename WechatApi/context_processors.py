__author__ = 'Swolfod'
# -*- coding: utf-8 -*-

from .config import *
from django.core.cache import cache

def default(request):
    jsapi_ticket = cache.get("jsapi_ticket")
    if not jsapi_ticket:
        access_token = cache.get("access_token")
        if not access_token:
            tokenUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(AppId, SecretKey)
            

    return dict(request=request, appId=AppId)