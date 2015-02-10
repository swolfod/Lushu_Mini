__author__ = 'Swolfod'
# -*- coding: utf-8 -*-

from .config import *
from django.core.cache import cache
from utilities import utils
import json
import time
import hashlib
from django.conf import settings

WECHAT_DEBUG = getattr(settings, "WECHAT_DEBUG", True)

def default(request):
    if WECHAT_DEBUG:
        return dict()

    jsapi_ticket = cache.get("jsapi_ticket")
    if not jsapi_ticket:
        access_token = cache.get("access_token")
        if not access_token:
            tokenUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(AppId, SecretKey)
            link, content, session = utils.LoadHttpString(tokenUrl)
            accessInfo = json.loads(content)
            access_token = accessInfo.get("access_token")
            if access_token:
                cache.set("access_token", access_token, 7200)

        if access_token:
            ticketUrl = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi".format(access_token)
            link, content, session = utils.LoadHttpString(ticketUrl)
            ticketInfo = json.loads(content)
            jsapi_ticket = ticketInfo.get("ticket")
            if jsapi_ticket:
                cache.set("jsapi_ticket", jsapi_ticket, 7200)

    signature = None
    timestamp = str(int(time.time()))
    if jsapi_ticket:
        rawStr = "jsapi_ticket={0}&noncestr={1}&timestamp={2}&url={3}".format(
            jsapi_ticket,
            NonceStr,
            timestamp,
            request.build_absolute_uri()
        )
        signature = hashlib.sha1(rawStr.encode("utf-8")).hexdigest()

    return dict(request=request, appId=AppId, timestamp=timestamp, nonceStr=NonceStr, signature=signature)