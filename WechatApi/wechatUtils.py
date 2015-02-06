__author__ = 'swolfod'

from .config import *
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from urllib.parse import quote_plus

def authenticated(request):
    code = request.session.get("code")
    refreshToken = request.session.get("refreshToken")
    userInfo = request.session.get("userInfo")

    return code is not None and refreshToken is not None and userInfo is not None


def wechatAuthUrl(request, state=""):
    return "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base&state={3}#wechat_redirect".format(
        AppId,
        quote_plus(request.build_absolute_uri(reverse("WechatApi.views.authCallback"))),
        state
    )


def requireWechatAuth(oriFunc):
    def wrapper(request):
        if authenticated(request):
            return oriFunc(request)

        return HttpResponseRedirect(wechatAuthUrl(request, quote_plus(request.build_absolute_uri())))

    return wrapper