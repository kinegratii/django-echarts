from django import template
from django_echarts.utils.burl import burl_kwargs

register = template.Library()


@register.simple_tag(takes_context=True)
def page_link(context, page_number):
    url = context['request'].get_full_path()
    return burl_kwargs(url, page=page_number)
