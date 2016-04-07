from django.conf.urls import url
from messages import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^messages/$', views.MessagesList.as_view()),
    url(r'^places/(?P<pk>[0-9]+)/$', views.MessagesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
