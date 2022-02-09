# coding=utf8
"""Template tags for django-echarts.

"""

from django import template

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.utils.interfaces import to_css_length, merge_js_dependencies

register = template.Library()


@register.simple_tag(takes_context=True)
def dep_url(context, dep_name: str, repo_name: str = None):
    return DJANGO_ECHARTS_SETTINGS.resolve_url(dep_name, repo_name)


@register.simple_tag(takes_context=True)
def echarts_container(context, echarts):
    return template.Template(
        '<div id="{chart_id}" style="width:{width};height:{height};"></div>'.format(
            chart_id=echarts.chart_id,
            width=to_css_length(echarts.width),
            height=to_css_length(echarts.height)
        )
    ).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    dependencies = merge_js_dependencies(*args)
    links = map(DJANGO_ECHARTS_SETTINGS.resolve_url, dependencies)

    return template.Template(
        '<br/>'.join(['<script src="{link}"></script>'.format(link=link) for link in links])
    ).render(context)


def build_echarts_initial_fragment(*charts):
    contents = []
    for chart in charts:
        content_fmt = '''
          var div_{chart_id} = document.getElementById('{chart_id}');
          var myChart_{chart_id} = echarts.init({init_params});
          var option_{chart_id} = {options};
          myChart_{chart_id}.setOption(option_{chart_id});
          '''
        div_v_name = "div_{0}".format(chart.chart_id)
        js_content = content_fmt.format(
            init_params=div_v_name,
            chart_id=chart.chart_id,
            options=chart.dump_options_with_quotes()
        )
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
