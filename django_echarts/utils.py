# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from .plugins.host import HostStore

# Default settings for django-echarts app
DEFAULT_SETTINGS = {
    'echarts_version': '3.7.0',
    'js_host': 'bootcdn'
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
        self._host_store = HostStore(name_or_host=self['js_host'], context={
            'STATIC_URL': settings.STATIC_URL,
            'echarts_version': self['echarts_version']
        })
        self.add_extra_item('js_host_url', self._host_store.host_url)

    def add_extra_item(self, name, value):
        self[name] = value

    @property
    def host_store(self):
        return self.host_store


def get_django_echarts_settings():
    project_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    project_settings.update(DEFAULT_SETTINGS)
    pro_settings = SettingsStore(**project_settings)
    return pro_settings


# The public API for project's settings
DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
