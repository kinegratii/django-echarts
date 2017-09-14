# coding=utf8

from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django_echarts.views.frontend import EChartsFrontView

from .demo_data import create_simple_bar, create_simple_kline, create_simple_map, create_simple_pie


class IndexView(TemplateView):
    template_name = 'index.html'


class FrontendEchartsTemplate(TemplateView):
    template_name = 'frontend_charts.html'


class SimpleBarView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return create_simple_bar()


class SimpleKLineView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return create_simple_kline()


class SimpleMapView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return create_simple_map()


class SimplePieView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return create_simple_pie()
