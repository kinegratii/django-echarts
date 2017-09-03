# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject
from pyecharts.constants import DEFAULT_HOST

# Default settings for django-echarts app
DEFAULT_SETTINGS = {
    'echarts_version': '3.7.0',
    'js_host': 'bootcdn'
}


class AttrDict(dict):
    """Add attribute access for a dict

    """

    JS_HOSTS = {
        'pyecharts': DEFAULT_HOST,
        'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
        'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
        'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}'
    }

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def enhance(self):
        self['js_host'] = self.build_js_host()

    def build_js_host(self):
        host_format = self.JS_HOSTS.get(self['js_host'], self['js_host'])
        return host_format.rstrip('/').format(
            static_url=settings.STATIC_URL,
            echarts_version=self['echarts_version']
        )


def get_django_echarts_settings():
    project_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    project_settings.update(DEFAULT_SETTINGS)
    pro_settings = AttrDict(**project_settings)
    pro_settings.enhance()
    return pro_settings


DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
