# coding=utf8

"""
Expose the settings objects.
"""

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from django_echarts.plugins.store import SettingsStore, DEFAULT_SETTINGS


def get_django_echarts_settings():
    project_echarts_settings = {k: v for k, v in DEFAULT_SETTINGS.items()}
    project_echarts_settings.update(getattr(settings, 'DJANGO_ECHARTS', {}))
    extra_settings = {
        'STATIC_URL': settings.STATIC_URL
    }
    settings_store = SettingsStore(
        echarts_settings=project_echarts_settings,
        extra_settings=extra_settings
    )
    return settings_store


DJANGO_ECHARTS_SETTINGS = SimpleLazyObject(get_django_echarts_settings)
