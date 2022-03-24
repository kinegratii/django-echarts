from functools import singledispatch

from prettytable import PrettyTable
from pyecharts.charts.base import Base
from pyecharts.components.table import Table

from .articles import ChartInfo
from .chart_widgets import NamedCharts
from .html_widgets import ValueItem, ValuesPanel
from .containers import RowContainer, Container
from .pages import WidgetCollection

__all__ = ['flat_chart', 'get_js_dependencies']


@singledispatch
def flat_chart(widget):
    """Get chart object list from a widget."""
    raise TypeError(f'Can not flat widget type: {widget.__class__.__name__}')


@flat_chart.register(Base)
def flat_base(widget: Base):
    return [widget]


@flat_chart.register(PrettyTable)
@flat_chart.register(Table)
@flat_chart.register(ValueItem)
@flat_chart.register(ValuesPanel)
@flat_chart.register(ChartInfo)
def flat_table(widget):
    return []


@flat_chart.register(NamedCharts)
@flat_chart.register(Container)
@flat_chart.register(RowContainer)
@flat_chart.register(WidgetCollection)
@flat_chart.register(tuple)
@flat_chart.register(list)
def flat_named_charts(widget):
    chart_list = []
    for chart in widget:
        chart_list.extend(flat_chart(chart))
    return chart_list


# @flat_chart.register(WidgetCollection)
# def flat_named_charts(widget: WidgetCollection):
#     chart_list = []
#     for chart in widget.charts:
#         chart_list.extend(flat_chart(chart))
#     return chart_list


_ECHARTS_LIB_NAMES = [
    'echarts.common', 'echarts.common.min',
    'echarts', 'echarts.min', 'echartsgl', 'echarts-gl', 'echarts-gl.min',
    'echarts.simple', 'echarts.simple.min',
    'extension/bmap', 'extension/bmap.min',
    'extension/dataTool', 'extension/dataTool.min'
]


def get_js_dependencies(widget, enable_theme=False):
    dep_list = []
    widget_list = []
    if isinstance(widget, (list, tuple)):
        for w in widget:
            if isinstance(w, str):
                dep_list.append(w)
            else:
                widget_list.append(w)
    elif isinstance(widget, str):
        dep_list.append(widget)
    else:
        widget_list.append(widget)
    chart_list = flat_chart(widget_list)

    def _deps(_chart):
        if isinstance(_chart.js_dependencies, list):
            return _chart.js_dependencies
        if hasattr(_chart.js_dependencies, 'items'):
            return list(_chart.js_dependencies.items)  # pyecharts.commons.utils.OrderedSet
        raise ValueError('Can not parse js_dependencies.')

    front_items = []
    for chart in chart_list:
        _dep_list = _deps(chart)

        for dep in _dep_list:
            if dep not in dep_list and dep not in front_items:
                if dep in _ECHARTS_LIB_NAMES:
                    front_items.append(dep)
                else:
                    dep_list.append(dep)
        if enable_theme and hasattr(chart, 'theme') and not chart.theme not in dep_list:
            dep_list.append(chart.theme)
    front_items.sort(key=lambda x: _ECHARTS_LIB_NAMES.index(x))
    return front_items + dep_list
