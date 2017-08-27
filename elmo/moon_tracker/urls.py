from django.conf.urls import url, include
from django.contrib import admin

from moon_tracker import views

urlpatterns = [
    url(r'system/(?P<system>.+)/(?P<planet>[0-9]+)/(?P<moon>[0-9]+)/$', views.moon_detail),
    url(r'system/(?P<system>.+)/$', views.moon_list),
    url(r'constellation/(?P<constellation>.+)/$', views.moon_list),
    url(r'region/(?P<region>.+)/$', views.moon_list),
]
