from django.conf.urls import url
from user_messages import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^messages/$', views.MessagesList.as_view()),
    url(r'^messages/(?P<message_pk>[0-9]+)/$', views.MessagesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
