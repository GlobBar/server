from django.conf.urls import url
from friends import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^relation/$', views.RelationList.as_view()),
    url(r'^followers/$', views.FollowerList.as_view()),
    url(r'^followings/$', views.FollowingsList.as_view()),
    url(r'^requests/$', views.RequestsList.as_view()),
    url(r'^requests/count/$', views.RequestsCountView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
