# coding=utf8

from __future__ import unicode_literals

from django.conf.urls import url, include

from demo import urls as demo_urls

from demo import frontend_views, backend_views

urlpatterns = [
    url(r'^$', frontend_views.IndexView.as_view()),
    url(r'^frontend_charts_list/$', frontend_views.FrontendEchartsTemplate.as_view()),
    url('^backend_charts_list/$', backend_views.BackendEChartsTemplate.as_view()),

    url(r'options/simpleBar/', frontend_views.SimpleBarView.as_view()),
    url(r'options/simpleKLine/', frontend_views.SimpleKLineView.as_view()),
    url(r'options/simpleMap/', frontend_views.SimpleMapView.as_view()),
    url(r'options/simplePie/', frontend_views.SimplePieView.as_view()),
    url(r'^demo/', include(demo_urls))
]
