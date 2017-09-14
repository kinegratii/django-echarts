# coding=utf8

from __future__ import unicode_literals

from django.views.generic.base import TemplateView

from demo import models
from pyecharts import Line

from django_echarts.views.backend import EChartsBackendView

from .demo_data import create_simple_bar, create_simple_kline, create_simple_map, create_simple_pie

ECHARTS_DICT = {
    'bar': create_simple_bar,
    'kine': create_simple_kline,
    'map': create_simple_map,
    'pie': create_simple_pie
}


class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        if name not in ECHARTS_DICT:
            name = 'bar'
        return ECHARTS_DICT[name]()


class TemperatureEChartsView(EChartsBackendView):
    echarts_instance_name = 'line'
    template_name = 'temperature_charts.html'

    def get_echarts_instance(self, **kwargs):
        context = super(TemperatureEChartsView, self).get_context_data(**kwargs)
        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)
        context['line'] = line
        return context
