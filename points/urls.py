from django.conf.urls import url
from points import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^points/$', views.PointsList.as_view()),
    url(r'^users/me/balance/$', views.BalanceUp.as_view()),
    url(r'^users/donate/$', views.BalanceDonate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
