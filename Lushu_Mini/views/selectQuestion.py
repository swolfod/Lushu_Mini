__author__ = 'swolfod'

from WechatApi import wechatUtils
from utilities.djangoUtils import secureRender
from Lushu_Mini.models import dataUtils


@wechatUtils.requireWechatAuth
def selectQuestion(request):
    account = wechatUtils.getCurrentAccount(request)
    questions = dataUtils.availableQuestions(account)

    return secureRender(request, "selectQuestion.html", {
        "account": account,
        "questions": questions
    })