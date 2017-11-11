from django.conf.urls import include, url
from rest_framework.authtoken import views as authviews
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^register/', views.CreateUser.as_view(), name='register'),
    url(r'^login/', views.LoginUser.as_view(), name='login'),
    url(r'^social/(?P<pk>[0-9]+)/$', views.UserInfo.as_view(), name='social'),
    url(r'^connect/(?P<pk>[0-9]+)/$', views.ConnectUser.as_view(), name='connect'),
    url(r'^web/(?P<pk>[0-9]+)/$', views.WebUserInfo.as_view(), name='web'),
]

urlpatterns = format_suffix_patterns(urlpatterns)