__author__ = 'swolfod'

from django.db import models


class WechatAccount(models.Model):
    unionid         = models.CharField(max_length=255, unique=True)
    nickname        = models.CharField(max_length=255)
    sex             = models.BooleanField(default=False)
    province        = models.CharField(max_length=255)
    city            = models.CharField(max_length=255)
    country         = models.CharField(max_length=255)
    headimgurl      = models.CharField(max_length=255)
    privilege       = models.CharField(max_length=255)

    class Meta:
        app_label = "WechatApi"
