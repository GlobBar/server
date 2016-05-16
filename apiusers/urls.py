from django.conf.urls import url
from apiusers import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^users/eml_register/$', views.UserEmailRegister.as_view()),
    url(r'^users/eml_login/$', views.UserEmailLogin.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^users/(?P<pk>me)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
