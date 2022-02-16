# coding=utf8


from django.views.generic.base import TemplateView
from django_echarts.views import EChartsFrontView

from .demo_data import FACTORY


class IndexView(TemplateView):
    template_name = 'index.html'


class FrontendEchartsTemplate(TemplateView):
    template_name = 'frontend_charts.html'


class SimpleBarView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORY.create('bar')


class SimpleMapView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORY.create('map')


class SimplePieView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORY.create('pie')


class WordCloudView(EChartsFrontView):
    def get_echarts_instance(self, *args, **kwargs):
        return FACTORY.create('word_cloud')
