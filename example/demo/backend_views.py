# coding=utf8

from __future__ import unicode_literals

from django.db.models import Count
from pyecharts import Line, Pie, Page, Bar

from django_echarts.views.backend import EChartsBackendView
from django_echarts.datasets.fetch import fetch
from demo import models
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


class PageDemoView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'page_demo.html'

    def get_echarts_instance(self, *args, **kwargs):
        device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
        device_types, counters = fetch(device_data, 'device_type', 'count')
        pie = Pie("设备分类", page_title='设备分类', width='100%')
        pie.add("设备分类", device_types, counters, is_label_show=True)

        battery_lifes = models.Device.objects.values('name', 'battery_life')
        names, lifes = fetch(battery_lifes, 'name', 'battery_life')
        bar = Bar('设备电量', page_title='设备电量', width='100%')
        bar.add("设备电量", names, lifes)
        page = Page.from_charts(pie, bar)
        return page
