from django.conf.urls import url, include
from django.contrib import admin

from moon_tracker import views

urlpatterns = [
    url(r'^system/(?P<system>.+)/(?P<planet>[0-9]+)/(?P<moon>[0-9]+)/$', views.moon_detail, name='moon_detail'),
    url(r'^system/(?P<system>.+)/$', views.list_system, name='list_system'),
    url(r'^constellation/(?P<constellation>.+)/$', views.list_constellation, name='list_constellation'),
    url(r'^region/(?P<region>.+)/$', views.list_region, name='list_region'),
    url(r'^$', views.list_universe, name='list_universe'),
]
