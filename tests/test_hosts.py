# coding=utf8

from __future__ import unicode_literals

import unittest

from django_echarts.plugins.hosts import HostStore, ECHARTS_LIB_HOSTS, ECHARTS_MAP_HOSTS


class HostStoreTestCase(unittest.TestCase):
    def test_lib_host(self):
        # Basic tests
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '3.7.0'
        }
        hs = HostStore.from_hosts(m_context, ECHARTS_LIB_HOSTS, 'bootcdn')
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            hs.generate_js_link('echarts.min')
        )

        self.assertEqual(
            'https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.0/echarts.min.js',
            hs.generate_js_link('echarts.min', js_host='cdnjs')
        )
        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            hs.generate_js_link(
                'echarts.min',
                js_host='https://cdn.bootcss.com/echarts/{echarts_version}'
            )
        )

    def test_map_host(self):
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '3.7.0'
        }
        hs = HostStore.from_hosts(m_context, ECHARTS_MAP_HOSTS, 'echarts')
        self.assertEqual(
            'https://chfw.github.io/jupyter-echarts/echarts/china.js',
            hs.generate_js_link('china', js_host='pyecharts')
        )
        # Add
        hs.add_host('https://amap.com/js', 'amap')
        self.assertEqual(
            'https://amap.com/js/fujian.js',
            hs.generate_js_link('fujian', 'amap')
        )
        self.assertEqual(
            'http://echarts.baidu.com/asset/map/js/china.js',
            hs.generate_js_link('china')
        )
