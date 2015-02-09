from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Lushu_Mini.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/', include('WechatApi.urls')),
)

urlpatterns += patterns('Lushu_Mini.views',
    (r"^$", "selectQuestion"),
    (r"^viewQuiz/(\d+)/$", "viewQuiz"),
    (r"^viewQuiz/(\d+)/([\w-]+)/$", "viewQuiz"),
    (r"^viewQuiz/(\d+)/([\w-]+)/([\w-]+)/$", "viewQuiz"),
    (r"^answerQuiz/$", "answerQuiz"),
    (r"^viewAnswers/(\d+)/$", "viewAnswers"),
    (r"^ajLikeAnswer/(\d+)/$", "ajLikeAnswer"),
)
