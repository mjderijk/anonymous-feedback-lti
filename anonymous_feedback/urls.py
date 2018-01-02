from django.conf.urls import url
from anonymous_feedback.views import LaunchView, SubmitView


urlpatterns = [
    url(r'^$', LaunchView.as_view()),
    url(r'submit$', SubmitView.as_view()),
]
