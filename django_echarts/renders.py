from functools import singledispatch

from borax.htmls import HTMLString, html_tag
from django.template import engines
from django.template.loader import get_template
from django.utils.html import SafeString
from django_echarts.entities import (
    ValuesPanel, ValueItem, LinkItem, Menu, NamedCharts, ChartInfo, DwString, RowContainer, Container
)
from prettytable import PrettyTable
from pyecharts.charts.base import Base
from pyecharts.components.table import Table


def _to_css_length(val):
    if isinstance(val, (int, float)):
        return '{}px'.format(val)
    else:
        return val


@singledispatch
def render_widget(widget, **kwargs) -> SafeString:
    # python3.8+ use typing.Protocol
    if hasattr(widget, '__html__') and callable(widget.__html__):
        return widget.__html__()
    message = f'<div>Unknown widget type:{widget.__class__.__name__}</div>'
    raise TypeError(message)
    # return SafeString(f'<div>Unknown widget type:{widget.__class__.__name__}</div>')


@render_widget.register(type(None))
def render_none(widget, **kwargs) -> SafeString:
    return SafeString('')


@render_widget.register(SafeString)
@render_widget.register(HTMLString)
def render_html(widget, **kwargs) -> SafeString:
    return widget


@render_widget.register(Base)
def render_chart(widget, **kwargs) -> SafeString:
    width = kwargs.get('width') or widget.width
    height = kwargs.get('height') or widget.height
    html = '<div id="{chart_id}" style="width:{width};height:{height};"></div>'.format(
        chart_id=widget.chart_id,
        width=_to_css_length(width),
        height=_to_css_length(height)
    )
    return SafeString(html)


@render_widget.register(Container)
def render_container(widget, **kwargs):
    tpl = get_template('widgets/container.html')
    return SafeString(tpl.render({'container': widget}))


@render_widget.register(NamedCharts)
@render_widget.register(RowContainer)
@render_widget.register(ValuesPanel)
def render_row_container(widget, **kwargs):
    tpl = get_template('widgets/row_container.html')
    return SafeString(tpl.render({'rc': widget}))


@render_widget.register(ChartInfo)
def render_chart_info(widget, **kwargs) -> SafeString:
    tpl = get_template('widgets/chart_info.html')
    return SafeString(tpl.render({'chart_info': widget}))


@render_widget.register(ValueItem)
def render_value_item(widget: ValueItem, **kwargs) -> SafeString:
    tpl = get_template('widgets/value_item.html')
    return SafeString(tpl.render({'item': widget}))


@render_widget.register(Table)
@render_widget.register(PrettyTable)
def render_table(widget, **kwargs) -> SafeString:
    if isinstance(widget, Table):
        html_content = widget.html_content
    else:
        html_content = widget.get_html_string(**kwargs)
    html_content = f'<div class="table-responsive">{html_content}</div>'
    return SafeString(html_content)


@render_widget.register(LinkItem)
@render_widget.register(Menu)
def render_link(widget, **kwargs) -> SafeString:
    context = kwargs.get('context')
    class_ = kwargs.get('class_')
    params = {'href': widget.url or 'javascript:;'}
    if isinstance(widget.text, DwString):
        django_engine = engines['django']
        template_obj = django_engine.from_string(widget.text)
        fields = ['request', ]
        context_dic = {}
        for f in fields:
            if f in context:
                context_dic[f] = context[f]
        params['content'] = template_obj.render(context_dic)
    else:
        params['content'] = widget.text
    if class_:
        params['class_'] = class_
    if isinstance(widget, LinkItem) and widget.new_page:
        params['target'] = '_blank'
    return html_tag('a', **params)
