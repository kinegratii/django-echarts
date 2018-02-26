# coding=utf8

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
            target_store.generate_js_link('echarts.min')
        )
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            target_store.generate_lib_js_link('echarts.min')
        )
        self.assertEqual(
            'http://echarts.baidu.com/asset/map/js/china.js.js',
            target_store.generate_map_js_link('china.js')
        )
