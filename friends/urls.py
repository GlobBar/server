from django.conf.urls import url
from friends import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^relation/$', views.RelationList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
