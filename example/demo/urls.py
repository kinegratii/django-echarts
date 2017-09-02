# coding=utf8

from __future__ import unicode_literals

from django.conf.urls import url

from demo import views

urlpatterns = [
    url(r'^temperature/$', views.TemperatureEChartsView.as_view()),
]
