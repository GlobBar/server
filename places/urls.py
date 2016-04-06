from django.conf.urls import url
from places import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^places/$', views.SnippetList.as_view()),
    url(r'^places/nearest/$', views.NearestSnippetList.as_view()),
    url(r'^places/$', views.SnippetList.as_view()),
    url(r'^places/saved/$', views.LikeList.as_view()),
    url(r'^places/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^places/checkin/$', views.CheckinList.as_view()),
    url(r'^places/like/$', views.LikeList.as_view()),
    url(r'^cities/$', views.CityList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
