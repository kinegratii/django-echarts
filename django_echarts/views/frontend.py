from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic.base import View

from .base import EChartsMixin


class EChartsFrontView(EChartsMixin, View):
    def get(self, request, **kwargs):
        echarts_instance = self.get_echarts_instance(**kwargs)
        return JsonResponse(data=echarts_instance.options, safe=False)
