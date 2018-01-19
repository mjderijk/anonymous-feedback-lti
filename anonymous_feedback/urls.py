from django.conf.urls import url
from anonymous_feedback.views import LaunchView
from anonymous_feedback.views.api import FormAPI, CommentsAPI, CommentAPI


urlpatterns = [
    url(r'^$', LaunchView.as_view()),
    url(r'^api/v1/form/(?P<course_id>[^/]*)$',
        FormAPI.as_view(), name='form-api'),
    url(r'^api/v1/form/(?P<course_id>[^/]*)/comments(?P<content_type>.csv)?$',
        CommentsAPI.as_view(), name='comments-api'),
    url(r'^api/v1/form/(?P<course_id>[^/]*)/comments/(?P<comment_id>[^/]*)$',
        CommentAPI.as_view(), name='comment-api'),
]
