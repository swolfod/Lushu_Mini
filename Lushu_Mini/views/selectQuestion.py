__author__ = 'swolfod'

from WechatApi import wechatUtils
from utilities.djangoUtils import respondJson
import json


@wechatUtils.requireWechatAuth
def selectQuestion(request):
    userInfo = request.session["userInfo"]
    return respondJson(json.loads(userInfo))