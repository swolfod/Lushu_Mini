__author__ = 'swolfod'

from Lushu_Mini.models import *
from WechatApi.models import WechatAccount
from utilities import djangoUtils


def getEntityById(model, entityId):
    return model.objects.get(pk=entityId)


def saveEntity(entity):
    entity.save()


def getAnswer(quiz, account):
    return djangoUtils.getOrNone(Answer, quiz=quiz, answerer=account)


def availableQuestions(account):
    return Question.objects.order_by("id").all()


def getQuiz(question, quizzer):
    return djangoUtils.getOrCreate(Quiz, question=question, quizzer=quizzer)


def getAnswerCnt(quiz):
    return quiz.answers.count()


def getAllAnswers(quiz):
    return quiz.answers.order_by("-id").all()


def alreadyLiked(account, answer):
    return answer.likedBy.filter(id=account.id).exists()


def likeAnswer(account, answer):
    if answer.answerer_id != account.id and not alreadyLiked:
        answer.liked += 1
        answer.likedBy.add(account)
        saveEntity(answer)
        return True

    return False