from functools import singledispatch

from borax.htmls import HTMLString, html_tag
from django.template import engines
from django.template.loader import get_template
from django.utils.html import SafeString
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.entities import ValuesPanel, LinkItem, Menu, NamedCharts, ChartInfo, DwString
from prettytable import PrettyTable
from pyecharts.charts.base import Base
from pyecharts.components.table import Table


def is_table(widget):
    return isinstance(widget, Table) or isinstance(widget, PrettyTable)


def _to_css_length(val):
    if isinstance(val, (int, float)):
        return '{}px'.format(val)
    else:
        return val


def wrap_with_grid(html_list, col_item_num: int = 1, cns: dict = None):
    cns = cns or {}
    row_cn = cns.get('row', 'row')
    col_cn = cns.get('col', 'col-md-{n}').format(n=int(12 / col_item_num))
    output_list = ['<div class="{}">'.format(row_cn)]
    for item_html in html_list:
        output_list.append('<div class="{}">{}</div>'.format(col_cn, item_html))
    output_list.append('</div>')
    return ''.join(output_list)


@singledispatch
def render_widget(widget, **kwargs) -> SafeString:
    # python3.8+ use typing.Protocol
    if hasattr(widget, '__html__') and callable(widget.__html__):
        return widget.__html__()
    return SafeString(f'<div>Unknown widget type:{widget.__class__.__name__}</div>')


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


@render_widget.register(NamedCharts)
def render_named_charts(widget: NamedCharts, **kwargs) -> SafeString:
    theme = DJANGO_ECHARTS_SETTINGS.theme
    width = kwargs.get('width')
    height = kwargs.get('height')
    html_list = []
    for schart in widget:
        html_list.append(render_widget(schart, width=width, height=height))
    return SafeString(wrap_with_grid(html_list, widget.col_chart_num, cns=theme.cns))


@render_widget.register(ChartInfo)
def render_chart_info(widget, **kwargs) -> SafeString:
    tpl = get_template('widgets/info_card.html')
    return SafeString(tpl.render({'chart_info': widget}))


@render_widget.register(ValuesPanel)
def render_values_panel(widget: ValuesPanel, **kwargs) -> SafeString:
    theme = DJANGO_ECHARTS_SETTINGS.theme
    tpl = get_template('widgets/values_panel.html')
    html_list = [tpl.render({'panel': item}) for item in widget]
    return SafeString(wrap_with_grid(html_list, widget.col_item_num, theme.cns))


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
