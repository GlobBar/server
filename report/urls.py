from django.conf.urls import url
from report import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^report/$', views.ReportList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
