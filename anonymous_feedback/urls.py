from django.conf.urls import url
from anonymous_feedback.views import LaunchView, CommentsFileView
from anonymous_feedback.views.api import FormAPI, CommentsAPI, CommentAPI


urlpatterns = [
    url(r'^$', LaunchView.as_view()),
    url(r'^(?P<course_id>[0-9]+)/files/comments$',
        CommentsFileView.as_view(), name='comments-file'),
    url(r'^api/v1/form/(?P<course_id>[0-9]+)$',
        FormAPI.as_view(), name='form-api'),
    url(r'^api/v1/form/(?P<course_id>[0-9]+)/comments$',
        CommentsAPI.as_view(), name='comments-api'),
    url(r'^api/v1/form/(?P<course_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)$',
        CommentAPI.as_view(), name='comment-api'),
]
