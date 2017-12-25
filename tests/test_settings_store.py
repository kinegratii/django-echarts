# coding=utf8

from __future__ import unicode_literals

import unittest

from django_echarts.plugins.store import SettingsStore


class SettingsWithStaticUrlTestCase(unittest.TestCase):
    def test_default_settings(self):
        target_store = SettingsStore(
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )
        self.assertIsNone(target_store.settings['local_host'])
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            target_store.generate_lib_js_link('echarts.min')
        )
