from functools import singledispatch

from django_echarts.entities import NamedCharts, WidgetCollection
from prettytable import PrettyTable
from pyecharts.charts.base import Base
from pyecharts.components.table import Table

__all__ = ['flat_chart', 'get_js_dependencies']


@singledispatch
def flat_chart(widget):
    raise TypeError(f'Can not flat widget type: {widget.__class__.__name__}')


@flat_chart.register(Base)
def flat_base(widget: Base):
    return [widget]


@flat_chart.register(PrettyTable)
@flat_chart.register(Table)
def flat_table(widget):
    return []


@flat_chart.register(NamedCharts)
@flat_chart.register(tuple)
@flat_chart.register(list)
def flat_named_charts(widget: NamedCharts):
    chart_list = []
    for chart in widget:
        chart_list.extend(flat_chart(chart))
    return chart_list


@flat_chart.register(WidgetCollection)
def flat_named_charts(widget: WidgetCollection):
    chart_list = []
    for chart in widget.charts:
        chart_list.extend(flat_chart(chart))
    return chart_list


def get_js_dependencies(widget, enable_theme=False):
    chart_list = flat_chart(widget)

    def _deps(_chart):
        if isinstance(_chart.js_dependencies, list):
            return _chart.js_dependencies
        if hasattr(_chart.js_dependencies, 'items'):
            return list(_chart.js_dependencies.items)  # pyecharts.commons.utils.OrderedSet
        raise ValueError('Can not parse js_dependencies.')

    dep_list = []
    for chart in chart_list:
        _dep_list = _deps(chart)
        for dep in _dep_list:
            if dep not in dep_list:
                dep_list.append(dep)
        if enable_theme and hasattr(chart, 'theme') and not chart.theme not in dep_list:
            dep_list.append(chart.theme)
    return dep_list
