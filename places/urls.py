from django.conf.urls import url
from places import views

urlpatterns = [
    url(r'^places/$', views.snippet_list),
    url(r'^places/(?P<pk>[0-9]+)/$', views.snippet_detail),
]