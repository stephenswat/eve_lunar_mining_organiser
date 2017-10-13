from django.conf.urls import url

from moon_tracker import views

urlpatterns = [
    url(r'^system/(?P<system>.+)/(?P<planet>[0-9]+)/(?P<moon>[0-9]+)/$', views.moon_detail, name='moon_detail'),
    url(r'^system/(?P<system>.+)/$', views.list_system, name='list_system'),
    url(r'^constellation/(?P<constellation>.+)/$', views.SolarSystemListView.as_view(), name='list_constellation'),
    url(r'^region/(?P<region>.+)/$', views.ConstellationListView.as_view(), name='list_region'),
    url(r'^submit/$', views.batch_submit, name='batch_submit'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<uid>\d+)$', views.profile, name='profile'),
    url(r'^$', views.RegionListView.as_view(), name='list_universe'),
]
