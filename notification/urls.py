from django.conf.urls import url
from notification import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^dev_token/$', views.NotificationList.as_view()),
    url(r'^send_mail/$', views.MailSending.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
