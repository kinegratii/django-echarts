# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject

# Default settings for django-echarts app
DEFAULT_SETTINGS = {
    'js_host': 'https://chfw.github.io/jupyter-echarts/echarts'
}


class AttrDict(dict):
    """Add attribute access for a dict

    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_django_echarts_settings():
    custom_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    project_settings = custom_settings.update(DEFAULT_SETTINGS)
    return AttrDict(project_settings)


DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
