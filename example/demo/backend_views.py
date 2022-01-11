# coding=utf8


from borax.datasets.fetch import fetch

from django.db.models import Count
from pyecharts.charts import Line, Pie, Page, Bar
from pyecharts import options as opts
from django_echarts.datasets.charts import NamedCharts
from django_echarts.views import EChartsBackendView

from demo import models
from .demo_data import FACTORY


class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        return FACTORY.create(name)

    def get_template_names(self):
        if self.request.GET.get('name') == 'word_cloud':
            return ['word_cloud.html']
        else:
            return super().get_template_names()


class TemperatureEChartsView(EChartsBackendView):
    echarts_instance_name = 'line'
    template_name = 'temperature_charts.html'

    def get_echarts_instance(self, **kwargs):
        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        hs, ds = zip(*t_data)

        line = Line().add_xaxis(
            ds
        ).add_yaxis("商家A", hs).add_yaxis(
            "商家B", [15, 25, 16, 55, 48, 8]).set_global_opts(
            title_opts=opts.TitleOpts(title="High Temperature", subtitle="我是副标题"))
        return line


class PageDemoView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'page_demo.html'

    def get_echarts_instance(self, *args, **kwargs):
        device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
        # device_types, counters = fetch(device_data, 'device_type', 'count')
        pie = Pie().add("设备分类", list(device_data))

        battery_lifes = models.Device.objects.values('name', 'battery_life')
        names, lifes = fetch(battery_lifes, 'name', 'battery_life')
        bar = Bar()
        bar.add_xaxis(names)
        bar.add_yaxis('设备电量', lifes)
        page = Page()
        page.add(pie, bar)
        return page

