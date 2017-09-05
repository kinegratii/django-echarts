# coding=utf8
"""Template tags for django-echarts.

"""

from __future__ import unicode_literals

import warnings

from django import template
from django.utils import six
from pyecharts.base import Base, json_dumps

from ..utils import DJANGO_ECHARTS_SETTING

register = template.Library()


@register.inclusion_tag('tags/echarts.html')
def echarts_options(echarts):
    assert isinstance(echarts, Base), 'A pyecharts.base.Base object is required.'
    return {
        'echarts_options': echarts.render_embed()
    }


@register.inclusion_tag('tags/echarts_js.html')
def echarts_js(echarts):
    warnings.warn('Tag echarts_js is Deprecated. Use echarts_scripts instead.')
    assert isinstance(echarts, Base), 'A pyecharts.base.Base object is required.'
    return {
        'js_host': DJANGO_ECHARTS_SETTING.js_host_url,
        'script_list': echarts.get_js_dependencies()
    }


@register.simple_tag(takes_context=True)
def echarts_js_dependencies(context, *args):
    links = []
    for option_or_name in args:
        if isinstance(option_or_name, Base):
            for js_name in option_or_name.get_js_dependencies():
                if js_name not in links:
                    links.append(js_name)
        elif isinstance(option_or_name, six.text_type):
            if option_or_name not in links:
                links.append(option_or_name)
    links = map(DJANGO_ECHARTS_SETTING.host_store.generate_js_link, links)

    return template.Template('<br/>'.join(['<script src="{link}"></script>'.format(link=l) for l in links])).render(
        context)


def convert_to_options_content(echarts):
    return json_dumps(echarts.option, indent=4)


@register.inclusion_tag('tags/echarts_js_content.html')
def echarts_js_content(*echarts_list):
    for e in echarts_list:
        if not isinstance(e, Base):
            raise TypeError('A pyecharts.base.Base object is required.')
        e.option_content = convert_to_options_content(e)
    return {
        'echarts_list': echarts_list
    }
