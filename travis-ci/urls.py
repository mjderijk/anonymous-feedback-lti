from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('anonymous_feedback.urls')),
]
