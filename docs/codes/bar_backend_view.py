# coding=utf8

from pyecharts import Bar
from django_echarts.views.backend import EChartsBackendView


class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        bar = Bar("我的第一个图表", "这里是副标题")
        bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
        return bar
