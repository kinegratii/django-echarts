# coding=utf8

"""
Expose the settings objects.
"""
import os
from django.conf import settings
from django.utils.functional import SimpleLazyObject

from django_echarts.core.settings_store import SettingsStore

__all__ = ['DJANGO_ECHARTS_SETTINGS']


def get_django_echarts_settings():
    project_echarts_settings = getattr(settings, 'DJANGO_ECHARTS', {})
    static_url = settings.STATIC_URL
    if settings.STATICFILES_DIRS:
        staticfiles_dir = str(settings.STATICFILES_DIRS[0])
    else:
        staticfiles_dir = os.path.join(str(settings.BASE_DIR), 'static')
    extra_settings = {
        'STATIC_URL': settings.STATIC_URL,
        'STATICFILES_DIRS': settings.STATICFILES_DIRS
    }
    settings_store = SettingsStore(
        echarts_settings=project_echarts_settings,
        extra_settings=extra_settings,
        static_url=static_url,
        staticfiles_dir=staticfiles_dir
    )
    return settings_store


DJANGO_ECHARTS_SETTINGS = SimpleLazyObject(get_django_echarts_settings)  # type: SettingsStore
