# coding=utf8

from __future__ import unicode_literals

from django.conf.urls import url

from demo import backend_views

urlpatterns = [
    url(r'^temperature/$', backend_views.TemperatureEChartsView.as_view()),
]
