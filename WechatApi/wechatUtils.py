__author__ = 'swolfod'

from .config import *
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from urllib.parse import quote_plus
from utilities import djangoUtils, utils
from .models import *
from django.conf import settings
from uuid import uuid1
from random import randint
import json
from datetime import datetime, timedelta

WECHAT_DEBUG = getattr(settings, "WECHAT_DEBUG", True)


def authenticated(request):
    if WECHAT_DEBUG:
        return True

    openid = request.session.get("openid")
    refreshToken = request.session.get("refreshToken")
    userInfo = request.session.get("userInfo")

    return openid is not None and refreshToken is not None and userInfo is not None


def wechatAuthUrl(request, state=""):
    return "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_base,snsapi_userinfo&state={2}#wechat_redirect".format(
        AppId,
        quote_plus(request.build_absolute_uri(reverse("WechatApi.views.authCallback"))),
        state
    )


def requireWechatAuth(oriFunc):
    def wrapper(request,  *args, **kwargs):
        if authenticated(request):
            return oriFunc(request,  *args, **kwargs)

        return HttpResponseRedirect(wechatAuthUrl(request, quote_plus(request.get_full_path())))

    return wrapper


def getAccountById(openid):
    return djangoUtils.getOrNone(WechatAccount, openid=openid)


def getCurrentAccount(request):
    openid = request.session.get("openid")
    if not WECHAT_DEBUG:
        accessToken = request.session.get("accessToken")
        accessExpiry = request.session.get("accessExpiry")
        if not accessToken or not accessExpiry or datetime.strptime(accessExpiry, '%Y-%m-%d %H:%M:%S') < datetime.now():
            refreshWechatToken(request, refreshToken=request.session["refreshToken"])
            openid = request.session["openid"]

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


def refreshWechatToken(request, code=None, refreshToken=None):
    if code:
        accessUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code".format(
            AppId,
            SecretKey,
            code
        )
    elif refreshToken:
        accessUrl = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}".format(AppId, refreshToken)
    else:
        raise Exception()

    link, content, session = utils.LoadHttpString(accessUrl, encoding="utf-8", timeout=10)
    accessInfo = json.loads(content)

    access_token = accessInfo["access_token"]
    accessExpires = int(accessInfo["expires_in"])
    openid = accessInfo["openid"]

    request.session["accessToken"] = access_token
    request.session["accessExpiry"] = (datetime.now() + timedelta(0, accessExpires)).strftime('%Y-%m-%d %H:%M:%S')
    request.session["refreshToken"] = accessInfo["refresh_token"]
    request.session["openid"] = openid
    request.session["scope"] = accessInfo["scope"]

    # Refresh token expires in 30 days
    request.session.set_expiry(3600 * 24 * 30)

    userInfoUrl = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN".format(access_token, openid)
    link, content, session = utils.LoadHttpString(userInfoUrl, session=session, encoding="utf-8", timeout=10)
    userInfo = json.loads(content)

    openid = userInfo["openid"]
    wechatAccount = djangoUtils.getOrNone(WechatAccount, openid=openid)
    if not wechatAccount:
        wechatAccount = WechatAccount(openid=openid)

    wechatAccount.nickname = userInfo["nickname"]
    wechatAccount.unionid = userInfo.get("unionid", None)
    wechatAccount.sex = int(userInfo.get("sex", 1)) == 1
    wechatAccount.province = userInfo.get("province", None)
    wechatAccount.city = userInfo.get("city", None)
    wechatAccount.country =  userInfo.get("country", None)
    wechatAccount.headimgurl = userInfo.get("headimgurl", None)
    wechatAccount.privilege = userInfo.get("privilege", None)

    wechatAccount.save()

    request.session["userInfo"] = content
