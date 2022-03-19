# coding=utf8
"""Template tags for django-echarts.

"""
from typing import Union

from django import template
from django.template.loader import render_to_string, get_template
from django.utils.html import SafeString
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.entities import (LinkItem, Menu)
from django_echarts.entities.widgettools import flat_chart, get_js_dependencies
from django_echarts.renders import (render_widget, render_values_panel, render_link, render_table)
from django_echarts.utils.burl import burl_kwargs

register = template.Library()


def _build_init_script(chart):
    if hasattr(chart, '_is_geo_chart'):
        chart.is_geo_chart = chart._is_geo_chart
    context = {'c': chart}

    return SafeString(render_to_string('snippets/echarts_init_script.tpl', context))


@register.simple_tag(takes_context=True)
def dep_url(context, dep_name: str, repo_name: str = None):
    return DJANGO_ECHARTS_SETTINGS.resolve_url(dep_name, repo_name)


@register.simple_tag(takes_context=True)
def echarts_container(context, *echarts, **kwargs):
    div_list = []
    for chart in echarts:
        div_list.append(render_widget(chart, context=context, **kwargs))
    return template.Template('<br/>'.join(div_list)).render(context)


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    dependencies = get_js_dependencies(args, enable_theme=DJANGO_ECHARTS_SETTINGS.opts.enable_echarts_theme)
    links = map(DJANGO_ECHARTS_SETTINGS.resolve_url, dependencies)

    return template.Template(
        '<br/>'.join(['<script src="{link}"></script>'.format(link=link) for link in links])
    ).render(context)


def build_echarts_initial_fragment(*args):
    contents = []
    chart_obj_list = flat_chart(args)
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


@register.simple_tag
def dw_table(table_obj, **kwargs):
    return render_table(table_obj, **kwargs)


@register.simple_tag
def dw_values_panel(panel):
    return render_values_panel(panel)


@register.simple_tag(takes_context=True)
def dw_widget(context, widget, **kwargs):
    return render_widget(widget, context=context, **kwargs)


@register.simple_tag
def dw_collection(collection):
    tpl = get_template('widgets/collection.html')
    return SafeString(tpl.render({'collection': collection}))


@register.simple_tag
def theme_js():
    theme = DJANGO_ECHARTS_SETTINGS.theme
    html = []
    for link in theme.js_urls:
        html.append(f'<script type="text/javascript" src="{link}"></script>')
    return SafeString(''.join(html))


@register.simple_tag
def theme_css():
    theme = DJANGO_ECHARTS_SETTINGS.theme
    html = []
    for link in theme.css_urls:
        html.append(f'<link href="{link}" rel="stylesheet">')
    return SafeString(''.join(html))


@register.simple_tag(takes_context=True)
def page_link(context, page_number: int):
    url = context['request'].get_full_path()
    return burl_kwargs(url, page=page_number)


@register.simple_tag(takes_context=True)
def dw_link(context, item: Union[LinkItem, Menu], class_: str = None):
    return render_link(item, context=context, class_=class_)
