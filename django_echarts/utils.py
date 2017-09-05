# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from .plugins.staticfiles import HostStore

# Default settings for django-echarts app
DEFAULT_SETTINGS = {
    'echarts_version': '3.7.0',
    'lib_js_host': 'bootcdn',
    'map_js_host': 'echarts'
}


class AttrDict(dict):
    """Add attribute access for a dict

    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class SettingsStore(AttrDict):
    def __init__(self, *args, **kwargs):
        super(SettingsStore, self).__init__(*args, **kwargs)
        self._host_store = None
        self.build()

    def build(self):
        self._host_store = HostStore(
            echarts_lib_name_or_host=self['lib_js_host'],
            echarts_map_name_or_host=self['map_js_host'],
            context={
                'STATIC_URL': settings.STATIC_URL,
                'echarts_version': self['echarts_version']
            })

    def add_extra_item(self, name, value):
        self[name] = value

    @property
    def host_store(self):
        return self._host_store


def get_django_echarts_settings():
    project_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    project_settings.update(DEFAULT_SETTINGS)
    pro_settings = SettingsStore(**project_settings)
    return pro_settings


# The public API for project's settings
DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
