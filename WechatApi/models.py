__author__ = 'swolfod'

from django.db import models


class WechatAccount(models.Model):
    unionid         = models.CharField(unique=True)
    nickname        = models.CharField()
    sex             = models.BooleanField()
    province        = models.CharField()
    city            = models.CharField()
    country         = models.CharField()
    headimgurl      = models.CharField()
    privilege       = models.CharField()

    class Meta:
        app_label = "WechatApi"
