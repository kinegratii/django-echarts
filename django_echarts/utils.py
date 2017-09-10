# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from .plugins.staticfiles import Host, HostStore

# Default settings for django-echarts app
DEFAULT_SETTINGS = {
    'echarts_version': '3.7.0',
    'lib_js_host': 'bootcdn',
    'map_js_host': 'echarts',
    'local_host': None
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
        self._host_context = {
            'echarts_version': self['echarts_version']
        }
        if settings.STATIC_URL is not None:
            self._host_context.update({'STATIC_URL': settings.STATIC_URL})
        self.pre_check_and_build()
        self.build()

    def pre_check_and_build(self):
        # Check local_host with settings.STATIC_URL
        if self['local_host'] is not None:
            if settings.STATIC_URL is None:
                raise ValueError("The local_host item requires a no-empty settings.STATIC_URL.")
            if not self['local_host'].startswith('{STATIC_URL}'):
                raise ValueError('The local_host must start with the value of settings.STATIC_URL"')

        if self['lib_js_host'] == 'local_host':
            self['lib_js_host'] = self['local_host']
        if self['map_js_host'] == 'local_host':
            self['map_js_host'] = self['local_host']

    def build(self):
        self._host_store = HostStore(
            echarts_lib_name_or_host=self['lib_js_host'],
            echarts_map_name_or_host=self['map_js_host'],
            context=self._host_context
        )

    def add_extra_item(self, name, value):
        self[name] = value

    @property
    def host_store(self):
        return self._host_store

    def create_local_host(self):
        if self['local_host']:
            return Host(self['local_host'], context=self._host_context)


def get_django_echarts_settings():
    project_settings = {k: v for k, v in DEFAULT_SETTINGS.items()}
    project_settings.update(getattr(settings, 'DJANGO_ECHARTS', {}))
    pro_settings = SettingsStore(**project_settings)
    return pro_settings


# The public API for project's settings
DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
