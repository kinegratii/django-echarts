# coding=utf8

from __future__ import unicode_literals

from django.views.generic.base import TemplateView

from .base import EChartsMixin


class EChartsBackendView(EChartsMixin, TemplateView):
    echarts_instance_name = 'echarts_instance'

    def get_context_data(self, **kwargs):
        context = super(EChartsBackendView, self).get_context_data(**kwargs)
        context[self.echarts_instance_name] = self.get_echarts_instance(**kwargs)
        return context
