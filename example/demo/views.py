# coding=utf8

from __future__ import unicode_literals

from demo import models
from pyecharts import Line

from django_echarts.views.backend import EChartsBackendView


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
