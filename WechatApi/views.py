__author__ = 'swolfod'

from django.http import *
from django.shortcuts import HttpResponseRedirect
from urllib.parse import unquote
from .wechatUtils import refreshWechatToken


def wechatSignature(request):
    echostr = request.GET.get("echostr")
    return HttpResponse(echostr)


def authCallback(request):
    state = request.GET.get("state", "")
    code = request.GET.get("code", None)

    if not code:
        return authFailed(request, state)

    try:
        refreshWechatToken(code)
        redirectUrl = unquote(state) if state else "/"
        return HttpResponseRedirect(redirectUrl)
    except:
        #return authFailed(request, state)
        raise


def authFailed(request, state=""):
    if not state:
        state = request.GET.get("state", "")

    return HttpResponse("<h1>ERROR</h1>")