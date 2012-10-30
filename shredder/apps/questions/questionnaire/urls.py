from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to


urlpatterns = patterns('apps.questions.questionnaire.views',
    url(r'^generate-questionnaire/$', 'generate_questionnaire', name="generate_questionnaire"),
)
