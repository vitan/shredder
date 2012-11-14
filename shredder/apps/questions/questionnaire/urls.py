from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to


urlpatterns = patterns('apps.questions.questionnaire.views',
    url(r'^$', redirect_to, {'url': 'generate-questionnaire'}),
    url(r'^generate-questionnaire/$', 'generate_questionnaire', name="generate_questionnaire"),
    url(r'^questionnaire-history/$', 'questionnaire_history', name="questionnaire_history"),
    url(r'^(?P<questionnaire_id>\d+)/$', 'questionnaire_display', name="questionnaire_display"),
)
