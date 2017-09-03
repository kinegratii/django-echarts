# coding=utf8

from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from pyecharts import Line

from demo import models


class TemperatureEChartsView(TemplateView):
    template_name = 'temperature_charts.html'

    def get_context_data(self, **kwargs):
        context = super(TemperatureEChartsView, self).get_context_data(**kwargs)
        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)
        context['line'] = line
        return context
