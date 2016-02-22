from django.conf.urls import url
from files import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^files/$', views.FileUploadView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

