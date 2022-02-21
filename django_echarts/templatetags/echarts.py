# coding=utf8
"""Template tags for django-echarts.

"""

from django import template

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.utils.interfaces import to_css_length, merge_js_dependencies
from django_echarts.core.charttools import NamedCharts

register = template.Library()


def _build_init_div_container(chart):
    return '<div id="{chart_id}" style="width:{width};height:{height};"></div>'.format(
        chart_id=chart.chart_id,
        width=to_css_length(chart.width),
        height=to_css_length(chart.height)
    )


def __build_init_div_container_for_page(page, cns=None):
    col_num = page.col_num
    cns = cns or {}
    row_cn = cns.get('row', 'row')
    col_cn = cns.get('col', 'col-md-{n}').format(n=int(12 / col_num))
    html_list = ['<div class="{}">'.format(row_cn)]
    for chart in page:
        html_list.append('<div class="{}">{}</div>'.format(col_cn, _build_init_div_container(chart)))
    html_list.append('</div>')
    return ''.join(html_list)


def _build_init_javascript(chart):
    content_fmt = '''
      var div_{chart_id} = document.getElementById('{chart_id}');
      var myChart_{chart_id} = echarts.init({init_params});
      var option_{chart_id} = {options};
      myChart_{chart_id}.setOption(option_{chart_id});
      window.addEventListener('resize',function(){{ myChart_{chart_id}.resize();}});
      '''
    init_params = [
        "div_{0}".format(chart.chart_id)
    ]
    if DJANGO_ECHARTS_SETTINGS.opts.enable_echarts_theme and chart.theme:
        init_params.append(f'"{chart.theme}"')
    return content_fmt.format(
        init_params=','.join(init_params),
        chart_id=chart.chart_id,
        options=chart.dump_options_with_quotes()
    )


@register.simple_tag(takes_context=True)
def dep_url(context, dep_name: str, repo_name: str = None):
    return DJANGO_ECHARTS_SETTINGS.resolve_url(dep_name, repo_name)


@register.simple_tag(takes_context=True)
def echarts_container(context, *echarts):
    theme = context['theme']
    div_list = []
    for chart in echarts:
        if isinstance(chart, NamedCharts):
            div_list.append(__build_init_div_container_for_page(chart, cns=theme.cns))
        else:
            div_list.append(_build_init_div_container(chart))
    return template.Template('<br/>'.join(div_list)).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    dependencies = merge_js_dependencies(*args, enable_theme=DJANGO_ECHARTS_SETTINGS.opts.enable_echarts_theme)
    links = map(DJANGO_ECHARTS_SETTINGS.resolve_url, dependencies)

    return template.Template(
        '<br/>'.join(['<script src="{link}"></script>'.format(link=link) for link in links])
    ).render(context)


def build_echarts_initial_fragment(*charts):
    contents = []
    for chart in charts:
        if isinstance(chart, NamedCharts):
            for schart in chart:
                js_content = _build_init_javascript(schart)
                contents.append(js_content)
        else:
            js_content = _build_init_javascript(chart)
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
