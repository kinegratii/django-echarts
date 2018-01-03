# coding=utf8
"""Template tags for django-echarts.

"""

from __future__ import unicode_literals

from django import template
from django.utils import six

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.utils.interfaces import dump_options_json

register = template.Library()


@register.simple_tag(takes_context=True)
def echarts_container(context, echarts):
    def ex_wh(x):
        if isinstance(x, (int, float)):
            return '{}px'.format(x)
        else:
            return x

    return template.Template(
        '<div id="{chart_id}" style="width:{width};height:{height};"></div>'.format(
            chart_id=echarts.chart_id,
            width=ex_wh(echarts.width),
            height=ex_wh(echarts.height)
        )
    ).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    dependencies = []

    def _add(_x):
        if _x not in dependencies:
            dependencies.append(_x)

    for a in args:
        if hasattr(a, 'js_dependencies'):
            for d in a.js_dependencies:
                _add(d)
        elif isinstance(a, six.text_type):
            _add(a)
    if len(dependencies) > 1:
        dependencies.remove('echarts')
        dependencies = ['echarts'] + list(dependencies)
    links = map(DJANGO_ECHARTS_SETTINGS.generate_js_link, dependencies)

    return template.Template(
        '<br/>'.join(['<script src="{link}"></script>'.format(link=l) for l in links])
    ).render(context)


def build_echarts_initial_fragment(*charts):
    contents = []
    for chart in charts:
        content_fmt = '''
          var myChart_{chart_id} = echarts.init(document.getElementById('{chart_id}'));
          var option_{chart_id} = {options};
          myChart_{chart_id}.setOption(option_{chart_id});
          '''
        js_content = content_fmt.format(
            chart_id=chart.chart_id,
            options=dump_options_json(chart.options, indent=4)
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
