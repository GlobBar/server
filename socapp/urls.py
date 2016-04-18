from django.conf.urls import url
from socapp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^fb/post/$', views.FbPosts.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
