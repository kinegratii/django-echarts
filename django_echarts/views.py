import json
from abc import abstractmethod
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.base import View


class EChartsMixin:
    """
    Base Mixin for build echarts instance
    """

    @abstractmethod
    def get_echarts_instance(self, *args, **kwargs):
        pass


class EChartsBackendView(EChartsMixin, TemplateView):
    echarts_instance_name = 'echarts_instance'

    def get_context_data(self, **kwargs):
        context = super(EChartsBackendView, self).get_context_data(**kwargs)
        context[self.echarts_instance_name] = self.get_echarts_instance(**kwargs)
        return context


class EchartsBackendGroupView(TemplateView):
    url_prefix = ''
    menu = []

    @classmethod
    def as_urls(cls):
        pass


class EChartsFrontView(EChartsMixin, View):
    def get(self, request, **kwargs):
        echarts_instance = self.get_echarts_instance(**kwargs)
        return JsonResponse(data=json.loads(echarts_instance.dump_options_with_quotes()), safe=False)
