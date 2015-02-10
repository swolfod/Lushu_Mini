__author__ = 'swolfod'

from WechatApi import wechatUtils
from utilities.djangoUtils import secureRender
from Lushu_Mini.models import dataUtils
from Lushu_Mini.models import *


@wechatUtils.requireWechatAuth
def viewQuiz(request, questionId, quizzerId=None, answererId=None):
    account = wechatUtils.getCurrentAccount(request)
    question = dataUtils.getEntityById(Question, questionId)

    quizzer = wechatUtils.getAccountById(quizzerId) if quizzerId else account
    quiz = dataUtils.getQuiz(question, quizzer)

    answerer = wechatUtils.getAccountById(answererId) if answererId else None
    answer = dataUtils.getAnswer(quiz, answerer) if answerer else None

    myAnswer = dataUtils.getAnswer(quiz, account)
    answered = quiz.answers.count()

    toShare = int(request.GET.get("toShare", 0))

    return secureRender(request, "viewQuiz.html", {
        "quizId": quiz.id,
        "account": account,
        "question": question,
        "quizzer": quizzer,
        "followed": False,
        "myAnswer": myAnswer,
        "answerer": answerer,
        "answer": answer,
        "answered": answered,
        "toShare": toShare
    })