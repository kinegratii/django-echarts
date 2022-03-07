# coding=utf8

import unittest

from django_echarts.core.settings_store import SettingsStore


class SettingsWithStaticUrlTestCase(unittest.TestCase):
    def test_default_settings(self):
        target_store = SettingsStore(
            echarts_settings={
                'lib_repo': 'bootcdn'
            },
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )
        # self.assertIsNone(target_store.settings['local_host'])
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/4.8.0/echarts.min.js',
            target_store.generate_js_link('echarts.min')
        )
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/4.8.0/echarts.min.js',
            target_store.generate_js_link('echarts.min')
        )
        self.assertEqual(
            'https://assets.pyecharts.org/assets/maps/china.js',
            target_store.generate_js_link('china.js')
        )
