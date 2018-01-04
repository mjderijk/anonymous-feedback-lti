from django.conf.urls import url
from anonymous_feedback.views import (
    LaunchView, EditView, CommentView, SubmitView)


urlpatterns = [
    url(r'^$', LaunchView.as_view()),
    url(r'edit$', EditView.as_view()),
    url(r'view$', CommentView.as_view()),
    url(r'submit$', SubmitView.as_view()),
]
