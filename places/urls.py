from django.conf.urls import url
from places import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^places/$', views.SnippetList.as_view()),
    url(r'^places/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^places/checkin/$', views.CheckinList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
