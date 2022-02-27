# coding=utf8
"""Template tags for django-echarts.

"""
from django import template
from django.template.loader import render_to_string
from django.utils.html import SafeString

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.core.charttools import NamedCharts, merge_js_dependencies, ChartCollection

register = template.Library()


def _to_css_length(val):
    if isinstance(val, (int, float)):
        return '{}px'.format(val)
    else:
        return val


def _build_init_div_container(chart, width=None, height=None):
    width = width or chart.width
    height = height or chart.height
    return '<div id="{chart_id}" style="width:{width};height:{height};"></div>'.format(
        chart_id=chart.chart_id,
        width=_to_css_length(width),
        height=_to_css_length(height)
    )


def __build_init_div_container_for_page(page, cns=None, width=None, height=None):
    col_num = page.col_chart_num
    cns = cns or {}
    row_cn = cns.get('row', 'row')
    col_cn = cns.get('col', 'col-md-{n}').format(n=int(12 / col_num))
    html_list = ['<div class="{}">'.format(row_cn)]
    for chart in page:
        html_list.append(
            '<div class="{}">{}</div>'.format(col_cn, _build_init_div_container(chart, width=width, height=height)))
    html_list.append('</div>')
    return ''.join(html_list)


def _build_init_script(chart):
    if hasattr(chart, '_is_geo_chart'):
        chart.is_geo_chart = chart._is_geo_chart
    context = {'c': chart}
    return SafeString(render_to_string('snippets/echarts_init_script.tpl', context))


@register.simple_tag(takes_context=True)
def dep_url(context, dep_name: str, repo_name: str = None):
    return DJANGO_ECHARTS_SETTINGS.resolve_url(dep_name, repo_name)


@register.simple_tag(takes_context=True)
def echarts_container(context, *echarts, width=None, height=None):
    theme = context['theme']
    div_list = []
    for chart in echarts:
        if isinstance(chart, NamedCharts):
            div_list.append(__build_init_div_container_for_page(chart, cns=theme.cns, width=width, height=height))
        else:
            div_list.append(_build_init_div_container(chart, width=width, height=height))
    return template.Template('<br/>'.join(div_list)).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    dependencies = merge_js_dependencies(*args, enable_theme=DJANGO_ECHARTS_SETTINGS.opts.enable_echarts_theme)
    links = map(DJANGO_ECHARTS_SETTINGS.resolve_url, dependencies)

    return template.Template(
        '<br/>'.join(['<script src="{link}"></script>'.format(link=link) for link in links])
    ).render(context)


def _flat_to_chart_list(obj):
    """
    ChartCollection - Chart
    ChartCollection - NamedCharts - chart
    """
    chart_obj_list = []

    def _add(_obj):
        if isinstance(_obj, (NamedCharts, tuple)):
            for _c in _obj:
                _add(_c)
        elif isinstance(_obj, ChartCollection):
            for _c in _obj.charts:
                _add(_c)
        elif hasattr(_obj, 'dump_options'):  # Mock like pyecharts chart
            chart_obj_list.append(_obj)
        else:
            raise TypeError(f'Unsupported chat type:{_obj.__class__.__name__}')

    _add(obj)
    return chart_obj_list


def build_echarts_initial_fragment(*args):
    contents = []
    chart_obj_list = _flat_to_chart_list(args)
    for chart in chart_obj_list:
        js_content = _build_init_script(chart)
        contents.append(js_content)
    return '\n'.join(contents)


@register.simple_tag(takes_context=True)
def echarts_js_content(context, *echarts):
    contents = build_echarts_initial_fragment(*echarts)
    return template.Template(
        '<script type="text/javascript">\n{}\n</script>'.format(contents)
    ).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_content_wrap(context, *charts):
    return template.Template(
        build_echarts_initial_fragment(*charts)
    ).render(context)


@register.inclusion_tag('info_card.html', takes_context=True)
def dje_info_cart(context, info, layout_opts):
    theme = context['theme']
    return {
        'chart_info': info,
        'layout_opts': layout_opts
    }


# ----- The following tags takes data object from the context, not the user's parameters. -----


@register.simple_tag(takes_context=True)
def theme_js(context):
    theme = context['theme']
    html = []
    for link in theme.js_urls:
        html.append(f'<script type="text/javascript" src="{link}"></script>')
    return SafeString(''.join(html))


@register.simple_tag(takes_context=True)
def theme_css(context):
    theme = context['theme']
    html = []
    for link in theme.css_urls:
        html.append(f'<link href="{link}" rel="stylesheet">')
    return SafeString(''.join(html))
