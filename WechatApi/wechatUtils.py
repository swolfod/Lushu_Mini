__author__ = 'swolfod'

from .config import *
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from urllib.parse import quote_plus
from utilities import djangoUtils
from .models import *
from django.conf import settings
from uuid import uuid1
from random import randint

WECHAT_DEBUG = getattr(settings, "WECHAT_DEBUG", True)


def authenticated(request):
    if WECHAT_DEBUG:
        return True

    openid = request.session.get("openid")
    refreshToken = request.session.get("refreshToken")
    userInfo = request.session.get("userInfo")

    return openid is not None and refreshToken is not None and userInfo is not None


def wechatAuthUrl(request, state=""):
    return "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state={2}#wechat_redirect".format(
        AppId,
        quote_plus(request.build_absolute_uri(reverse("WechatApi.views.authCallback"))),
        state
    )


def requireWechatAuth(oriFunc):
    def wrapper(request,  *args, **kwargs):
        if authenticated(request):
            return oriFunc(request,  *args, **kwargs)

        return HttpResponseRedirect(wechatAuthUrl(request, quote_plus(request.build_absolute_uri())))

    return wrapper


def getAccountById(openid):
    return djangoUtils.getOrNone(WechatAccount, openid=openid)


def getCurrentAccount(request):
    openid = request.session.get("openid")
    account = getAccountById(openid)

    if not account and WECHAT_DEBUG:
        account = WechatAccount(
            openid = uuid1().hex,
            nickname = DEBUG_USERS[randint(0, len(DEBUG_USERS) - 1)],
            sex = randint(0, 1) == 0,
            headimgurl = DEBUG_AVATARS[randint(0, len(DEBUG_AVATARS) - 1)]
        )

        account.save()
        request.session["openid"] = account.openid

        return account

    return account