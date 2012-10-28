from django.conf.urls.defaults import patterns, include, url

from apps.questions.question.views import *

urlpatterns = patterns('apps.questions.question.views',
    # url(r'^$', 'shredder.views.home', name='home'),
    # url(r'^shredder/', include('shredder.foo.urls')),
     url(r'^share-my-question/', share_question, name="share_question"),
)
