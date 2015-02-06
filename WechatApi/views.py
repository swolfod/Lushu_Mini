__author__ = 'swolfod'

from .config import *
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import HttpResponseRedirect
import datetime
import json
from urllib.parse import quote_plus, unquote
from .wechatUtils import wechatAuthUrl
from utilities import utils, djangoUtils
from .models import WechatAccount


def wechatSignature(request):
    echostr = request.GET.get("echostr")
    return HttpResponse(echostr)


def authCallback(request):
    state = request.GET.get("state", "")
    code = request.GET.get("code", None)

    if not code:
        return authFailed(request, state)

    try:
        accessUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code".format(
            AppId,
            SecretKey,
            code
        )

        link, content, session = utils.LoadHttpString(accessUrl, timeout=10)
        accessInfo = json.loads(content)

        access_token = accessInfo["access_token"]
        accessExpires = int(accessInfo["expires_in"])
        openid = accessInfo["openid"]

        request.session["accressToken"] = access_token
        request.session["accessExpiry"] = (datetime.datetime.now() + datetime.timedelta(0, accessExpires)).strftime('%Y-%m-%d %H:%M:%S')
        request.session["refreshToken"] = accessInfo["refresh_token"]
        request.session["openid"] = openid
        request.session["scope"] = accessInfo["scope"]

        # Refresh token expires in 30 days
        request.session.set_expiry(3600 * 24 * 30)

        userInfoUrl = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN".format(access_token, openid)
        link, content, session = utils.LoadHttpString(userInfoUrl, session=session, timeout=10)
        userInfo = json.loads(content)

        unionid = userInfo["unionid"]
        wechatAccount = djangoUtils.getOrNone(WechatAccount, unionid=unionid)
        if not wechatAccount:
            wechatAccount = WechatAccount(unionid=unionid)

        wechatAccount.nickname = userInfo["nickname"]
        wechatAccount.sex = int(userInfo["sex"]) == 1
        wechatAccount.province = userInfo["province"]
        wechatAccount.city = userInfo["city"]
        wechatAccount.country = userInfo["country"]
        wechatAccount.headimgurl = userInfo["headimgurl"]
        wechatAccount.privilege = userInfo["privilege"]

        wechatAccount.save()

        request.session["userInfo"] = content

        redirectUrl = unquote(state) if state else "/"
        return HttpResponseRedirect(redirectUrl)
    except:
        return authFailed(request, state)


def authFailed(request, state=""):
    if not state:
        state = request.GET.get("state", "")

    return HttpResponseRedirect(wechatAuthUrl(request, state))