__author__ = 'swolfod'

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from WechatApi import wechatUtils
from Lushu_Mini.models import dataUtils
from Lushu_Mini.models import *
from utilities.djangoUtils import secureRender, respondJson, respondErrorJson


@wechatUtils.requireWechatAuth
def answerQuiz(request):
    quizId = request.POST["quizId"]
    place = request.POST["place"].strip()
    reason = request.POST["reason"].strip()

    if not place:
        return HttpResponseBadRequest()

    quiz = dataUtils.getEntityById(Quiz, quizId)

    account = wechatUtils.getCurrentAccount(request)
    if account.id == quiz.quizzer_id:
        return HttpResponseBadRequest()

    answer = dataUtils.getAnswer(quiz, account)
    if not answer:
        answer = Answer(quiz=quiz, answerer=account)

    answer.answer = place
    answer.description = reason
    answer.liked = 0
    dataUtils.saveEntity(answer)

    return HttpResponseRedirect(reverse("Lushu_Mini.views.viewAnswers", args=(quizId,)))


@wechatUtils.requireWechatAuth
def viewAnswers(request, quizId):
    account = wechatUtils.getCurrentAccount(request)

    quiz = dataUtils.getEntityById(Quiz, quizId)
    myAnswer = dataUtils.getAnswer(quiz, account)
    answers = dataUtils.getAllAnswers(quiz)

    if account.id != quiz.quizzer_id and not myAnswer:
        return HttpResponseRedirect(reverse("Lushu_Mini.views.viewQuiz", args=(quiz.question_id, quiz.quizzer.openid)))

    for answer in answers:
        if answer.answerer_id != account.id:
            answer.alreadyLiked = dataUtils.alreadyLiked(account, answer)

    if myAnswer:
        shareUrl = request.build_absolute_uri(reverse("Lushu_Mini.views.viewQuiz", args=(quiz.question_id, quiz.quizzer.openid, account.openid)))
    else:
        shareUrl = request.build_absolute_uri(reverse("Lushu_Mini.views.viewQuiz", args=(quiz.question_id, quiz.quizzer.openid)))
    shareUrl  += "?toShare=1"

    return secureRender(request, "quizAnswers.html", {
        "quiz": quiz,
        "account": account,
        "myAnswer": myAnswer,
        "answers": answers,
        "shareUrl": shareUrl,
        "quizImageUrl": request.build_absolute_uri(quiz.question.imageUrl)
    })


@wechatUtils.requireWechatAuth
def ajLikeAnswer(request, answerId):
    account = wechatUtils.getCurrentAccount(request)
    answer = dataUtils.getEntityById(Answer, answerId)

    if answer.answerer_id == account.id:
        return HttpResponseBadRequest()

    if dataUtils.likeAnswer(account, answer):
        return respondJson({
            "liked": answer.liked
        })
    else:
        return respondErrorJson(_("Already liked"))