__author__ = 'swolfod'

from django.db import models
from WechatApi.models import WechatAccount


class Question(models.Model):
    question        = models.CharField(max_length=255)
    description     = models.CharField(max_length=255)
    imageUrl        = models.CharField(max_length=255)

    def __str__(self):
        return self.question

    class Meta:
        app_label = "Lushu_Mini"


class Quiz(models.Model):
    question        = models.ForeignKey(Question, related_name="quizzes")
    quizzer         = models.ForeignKey(WechatAccount, related_name="quizzes")

    class Meta:
        app_label = "Lushu_Mini"

        unique_together = [
            ["quizzer", "question"],
        ]


class Answer(models.Model):
    quiz            = models.ForeignKey(Quiz, related_name="answers")
    answerer        = models.ForeignKey(WechatAccount, related_name="answers")
    answer          = models.CharField(max_length=255)
    description     = models.CharField(max_length=255)
    liked           = models.IntegerField()
    likedBy         = models.ManyToManyField(WechatAccount, related_name="+")

    class Meta:
        app_label = "Lushu_Mini"

        index_together = [
            ["quiz", "answerer"],
        ]