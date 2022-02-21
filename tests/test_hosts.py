# coding=utf8


import unittest

from django_echarts.core.dms import DependencyManager


class DependencyManagerTestCase(unittest.TestCase):
    def test_lib_host(self):
        # Basic tests
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '3.7.0'
        }
        manager = DependencyManager.create_default(
            context=m_context,
            repo_name='bootcdn',
        )

        self.assertEqual(
            'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
            manager.resolve_url('echarts.min')
        )

        self.assertEqual(
            'https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.0/echarts.min.js',
            manager.resolve_url('echarts.min', repo_name='cdnjs')
        )

    def test_map_host(self):
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '3.7.0'
        }
        manager = DependencyManager.create_default(
            context=m_context,
        )
        self.assertEqual(
            'https://echarts-maps.github.io/echarts-china-provinces-js/china.js',
            manager.resolve_url('china', repo_name='china-provinces')
        )
        # Add
        manager.add_repo('amap', 'https://amap.com/js', catalog='map')
        self.assertEqual(
            'https://amap.com/js/fujian.js',
            manager.resolve_url('fujian', 'amap')
        )


class CustomHostTestCase(unittest.TestCase):
    def test_add_host(self):
        m_context = {
            'echarts_version': '3.8.5'
        }

        manager = DependencyManager.create_default(
            context=m_context,
            repo_name='pyecharts'
        )
        manager.add_repo('demo', '/demo/', catalog='map')
        manager.add_repo('demo2', '/demo2/{echarts_version}', catalog='map')
        self.assertEqual(
            '/demo/fujian.js',
            manager.resolve_url('fujian', repo_name='demo')
        )
        self.assertEqual(
            '/demo2/3.8.5/fujian.js',
            manager.resolve_url('fujian', repo_name='demo2')
        )
