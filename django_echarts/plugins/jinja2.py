# coding=utf8
"""
A callable environment for django + jinjia2 + pyecharts.
"""

from __future__ import unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.conf import settings

from pyecharts.conf import PyEchartsConfig
from pyecharts.engine import BaseEnvironment


def environment(**options):
    """
    Create a environment object for settings.TEMPLATE.Jinja2.ENGINE
    :param options:
    :return:
    """
    env = BaseEnvironment(pyecharts_config=PyEchartsConfig(jshost=settings.STATIC_URL), **options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
