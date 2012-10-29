from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to


urlpatterns = patterns('apps.questions.question.views',
    url(r'^$', redirect_to, {'url': 'share-my-question'}),
    url(r'^share-my-question/$', 'share_question', name="share_question"),
)
