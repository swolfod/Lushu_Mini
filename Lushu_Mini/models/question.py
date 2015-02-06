__author__ = 'swolfod'

from django.db import models
from WechatApi.models import WechatAccount


class Question(models.Model):
    question        = models.CharField()
    imageUrl        = models.CharField()

    class Meta:
        app_label = "PieceMini"


class Answer(models.Model):
    account         = models.ForeignKey(WechatAccount, related_name="answers")
    question        = models.ForeignKey(Question, related_name="answers")
    liked           = models.IntegerField()
    likedBy         = models.ManyToManyField(WechatAccount, related_name="+")

    class Meta:
        app_label = "PieceMini"
