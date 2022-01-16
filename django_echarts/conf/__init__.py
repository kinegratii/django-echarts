# coding=utf8

"""
Expose the settings objects.
"""

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from django_echarts.dms.core import SettingsStore

__all__ = ['DJANGO_ECHARTS_SETTINGS']


def get_django_echarts_settings():
    project_echarts_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    extra_settings = {
        'STATIC_URL': settings.STATIC_URL
    }
    settings_store = SettingsStore(
        echarts_settings=project_echarts_settings,
        extra_settings=extra_settings
    )
    return settings_store


DJANGO_ECHARTS_SETTINGS = SimpleLazyObject(get_django_echarts_settings)  # type: SettingsStore
