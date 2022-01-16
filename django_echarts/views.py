import json
from abc import abstractmethod

from django.http import JsonResponse, Http404
from django.urls import path
from django.views.generic.base import View, TemplateView


class EChartsMixin:
    """
    Base Mixin for build echarts instance
    """

    @abstractmethod
    def get_echarts_instance(self, *args, **kwargs):
        pass


class EChartsBackendView(EChartsMixin, TemplateView):
    echarts_instance_name = 'echarts_instance'
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super(EChartsBackendView, self).get_context_data(**kwargs)
        context[self.echarts_instance_name] = self.get_echarts_instance(**kwargs)
        context['title'] = self.get_dje_page_title()
        return context

    def get_dje_page_title(self):
        return self.page_title


class EChartsFrontView(EChartsMixin, View):
    def get(self, request, **kwargs):
        echarts_instance = self.get_echarts_instance(**kwargs)
        return JsonResponse(data=json.loads(echarts_instance.dump_options_with_quotes()), safe=False)


# -------------------------- scaffolds --------------------

class SimpleChartBDView(EChartsBackendView):
    template_name = 'dje_simple_chart.html'
    page_title = 'My Chart'


class MultipleChartsBDView(EChartsBackendView):
    template_name = 'dje_multiple_charts.html'
    echarts_instance_name = 'charts'
    page_title = 'My Charts'


class SelectOneChartBDView(TemplateView):
    template_name = 'dje_selectone_chart.html'
    url_prefix = 'chart/<slug:name>'
    url_name = ''
    charts_config = []
    page_title = '{description}'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        context['title'] = 'My Charts'
        chart_name = self.kwargs.get('name')
        context['menu'] = []
        found = False
        for values in self.charts_config:
            name, description, *_ = values
            if chart_name == name and not found:
                found = True
                func = getattr(self, f'dje_chart_{name}', None)
                if func:
                    chart_obj = func()
                    context['chart_obj'] = chart_obj
                context['title'] = self.page_title.format(name=name, description=description)
                context['menu'].append((name, description, True))
            else:
                context['menu'].append((name, description, False))
        if found:
            tpl = 'dje_selectone_chart.html'
        else:
            tpl = 'dje_selectone_empty.html'
        return self.response_class(
            request=self.request,
            template=tpl,
            context=context,
            using=self.template_engine
        )

    @classmethod
    def urls(cls):
        kw = {}
        if cls.url_name:
            kw.update({'name': cls.url_name})
        return [
            path(cls.url_prefix, cls.as_view(), **kw)
        ]
