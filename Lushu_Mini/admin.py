__author__ = 'swolfod'

from django.contrib import admin
from .models import *
from WechatApi.models import WechatAccount


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'description')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('quizzer', 'question')
    inlines = [AnswerInline]


@admin.register(WechatAccount)
class WechatAccountAdmin(admin.ModelAdmin):
    list_display = ('nickname', )
