# coding=utf8

from __future__ import unicode_literals

import unittest

from django_echarts.plugins.staticfiles import HostStore


class ATest(unittest.TestCase):
    def test_all(self):
        # Basic tests
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '3.7.0'
        }
        hs = HostStore(m_context, 'bootcdn', 'echarts')
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            hs.generate_js_link('echarts.min')
        )
        self.assertEqual(
            'http://echarts.baidu.com/asset/map/js/china.js',
            hs.generate_js_link('china')
        )
        # Use custom js_host
        self.assertEqual(
            'https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.0/echarts.min.js',
            hs.generate_js_link('echarts.min', js_host='cdnjs')
        )
        self.assertEqual(
            'https://chfw.github.io/jupyter-echarts/echarts/china.js',
            hs.generate_js_link('china', js_host='pyecharts')
        )
        # Add
        hs.add_new_host('map', 'https://amap.com/js', 'amap')
        self.assertEqual(
            'https://amap.com/js/fujian.js',
            hs.generate_js_link('fujian', 'amap')
        )

