from django.conf.urls import url
from report import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^report/$', views.ReportList.as_view()),
    url(r'^city_reports/$', views.ReportsByPeriod.as_view()),
    url(r'^report/image/like/$', views.ReportImageLikeDetail.as_view()),
    url(r'^report/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
