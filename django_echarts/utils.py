# coding=utf8

from __future__ import unicode_literals

from django.conf import settings
from django.utils.functional import SimpleLazyObject

DEFAULT_SETTINGS = {
    'js_host': 'https://chfw.github.io/jupyter-echarts/echarts'
}


def get_django_echarts_settings():
    custom_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    project_settings = custom_settings.update(DEFAULT_SETTINGS)
    return project_settings


DJANGO_ECHARTS_SETTING = SimpleLazyObject(get_django_echarts_settings)
