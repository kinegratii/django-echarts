# coding=utf8


from borax.datasets.fetch import fetch
from pyecharts import options as opts
from pyecharts.charts import Line, Bar

from demo import models
from django_echarts.datasets.charts import NamedCharts
from django_echarts.views import EChartsBackendView, SimpleChartBDView, MultipleChartsBDView, SelectOneChartBDView
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


class MyFistBackendChartsTemplateView(SimpleChartBDView):
    page_title = '图表示例'

    def get_echarts_instance(self, *args, **kwargs):
        return FACTORY.create('bar')


class PageDemoView(MultipleChartsBDView):
    template_name = 'page_demo.html'
    echarts_instance_name = 'page'

    def get_echarts_instance(self, *args, **kwargs):
        bar0 = FACTORY.create('bar')

        battery_lifes = models.Device.objects.values('name', 'battery_life')
        names, lifes = fetch(battery_lifes, 'name', 'battery_life')
        bar = Bar().add_xaxis(names).add_yaxis('设备电量', lifes)
        page = NamedCharts().add([bar0, bar])
        return page


class MySelectChartView(SelectOneChartBDView):
    url_name = 'my_select_chart'
    url_prefix = 'chart/<slug:name>/'
    charts_config = [
        ('c1', '柱形图'),
        ('c2', '饼图')
    ]

    def dje_chart_c1(self, *args, **kwargs):
        return FACTORY.create('bar')

    def dje_chart_c2(self, *args, **kwargs):
        return FACTORY.create('pie')
