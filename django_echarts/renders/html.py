from functools import singledispatch

from borax.htmls import HTMLString, html_tag
from borax.strings import camel2snake
from django.template import engines
from django.template.loader import get_template
from django.utils.safestring import SafeString
from prettytable import PrettyTable
from pyecharts.charts.base import Base
from pyecharts.components.table import Table

from django_echarts.entities import (
    ValuesPanel, LinkItem, Menu, NamedCharts, DwString, RowContainer, Container, HTMLBase
)


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
@render_widget.register(HTMLBase)
@render_widget.register(NamedCharts)
@render_widget.register(RowContainer)
@render_widget.register(ValuesPanel)
def render_with_tpl(widget, **kwargs) -> SafeString:
    if 'tpl' in kwargs:
        tpl_name = kwargs['tpl']
    else:
        widget_name = camel2snake(widget.__class__.__name__)
        if widget_name in ('values_panel', 'named_charts'):
            widget_name = 'row_container'
        elif widget_name == 'widget_collection':
            widget_name = 'container'
        tpl_name = 'widgets/{}.html'.format(widget_name)
    tpl = get_template(tpl_name)
    return SafeString(tpl.render({'widget': widget}))


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
