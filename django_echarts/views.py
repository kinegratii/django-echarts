import warnings
import json
from abc import abstractmethod

from django.http import JsonResponse
from django.urls import path
from django.utils.text import slugify
from django.views.generic.base import View, TemplateView

from django_echarts.entities.chart_widgets import ChartInfo

warnings.warn('This module has been deprecated and will be removed in future version.', DeprecationWarning)


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

    def get_dje_page_title(self, *args, **kwargs):
        return self.page_title


class EChartsFrontView(EChartsMixin, View):
    def get(self, request, **kwargs):
        echarts_instance = self.get_echarts_instance(**kwargs)
        return JsonResponse(data=json.loads(echarts_instance.dump_options_with_quotes()), safe=False)


# -------------------------- scaffolds no theme --------------------

class SimpleChartBDView(EChartsBackendView):
    template_name = 'dje_simple_chart.html'
    page_title = 'My Chart'


class MultipleChartsBDView(EChartsBackendView):
    template_name = 'dje_multiple_charts.html'
    echarts_instance_name = 'charts'
    page_title = 'My Charts'


def as_chart(function=None, *, name=None, description=None):
    def decorator(func):
        cname = name or func.__name__
        func.chart_info = ChartInfo(name=cname, description=description)
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)


class SelectOneChartBDView(TemplateView):
    template_name = 'dje_selectone_chart.html'
    url_prefix = 'chart/<slug:name>'
    view_name = ''
    page_title = '{description}'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.view_name
        context['title'] = 'My Charts'
        chart_name = self.kwargs.get('name')
        context['menu'] = []
        found = False
        for info, func in self.get_chart_info():
            if chart_name == info.name and not found:
                found = True
                chart_obj = func(self)
                context['chart_obj'] = chart_obj
                context['title'] = self.get_dje_page_title(name=info.name, description=info.description)
                context['menu'].append((info.name, info.description, True))
            else:
                context['menu'].append((info.name, info.description, False))
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

    def get_dje_page_title(self, name, description, **kwargs):
        return self.page_title.format(name=name, description=description)

    def get_chart_info(self):
        for name, value in self.__class__.__dict__.items():
            if callable(value) and hasattr(value, 'chart_info') and isinstance(value.chart_info, ChartInfo):
                yield value.chart_info, value

    @classmethod
    def attach_view_name(cls):
        if cls.view_name:
            return cls.view_name
        end_s = ['BDView', 'View']
        s = cls.__name__
        for es in end_s:
            if s.endswith(es):
                view_name = slugify(s[:-len(es)])
                cls.view_name = view_name
                return view_name

    @classmethod
    def urls(cls):
        kw = {}
        view_name = cls.attach_view_name()
        if view_name:
            kw.update({'name': cls.view_name})
        return [
            path(cls.url_prefix, cls.as_view(), **kw)
        ]
