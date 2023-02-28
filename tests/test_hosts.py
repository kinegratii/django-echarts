# coding=utf8


import unittest

from django_echarts.core.dms import DependencyManager


class DependencyManagerTestCase(unittest.TestCase):
    def test_lib_host(self):
        # Basic tests
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '4.8.0',
            'baidu_map_ak': 'foo23zoo'
        }
        manager = DependencyManager.create_default(
            context=m_context,
            repo_name='bootcdn',
        )
        manager.add_repo('bootcdn', repo_url='https://cdn.bootcss.com/echarts/{echarts_version}/')

        self.assertEqual(
            'https://cdn.bootcss.com/echarts/4.8.0/echarts.min.js',
            manager.resolve_url('echarts.min')
        )
        self.assertEqual('https://api.map.baidu.com/api?v=2.0&ak=foo23zoo',
                         manager.resolve_url('https://api.map.baidu.com/api?v=2.0&ak=xxx'))

    def test_map_host(self):
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '4.8.0'
        }
        manager = DependencyManager.create_default(
            context=m_context,
        )
        manager.add_repo('china-provinces', repo_url='https://echarts-maps.github.io/echarts-china-provinces-js/')
        self.assertEqual(
            'https://echarts-maps.github.io/echarts-china-provinces-js/maps/china.js',
            manager.resolve_url('china', repo_name='china-provinces')
        )
        # Add
        manager.add_repo('amap', 'https://amap.com/js')
        self.assertEqual(
            'https://amap.com/js/fujian.js',
            manager.resolve_url('fujian', 'amap')
        )

    def test_custom_d2u(self):
        m_context = {
            'STATIC_URL': '/static/',
            'echarts_version': '4.8.0',
            'baidu_map_ak': 'foo'
        }
        manager = DependencyManager.create_default(
            context=m_context
        )
        manager.load_from_dep2url_dict({
            'baidu_map_api': 'https://api.map.baidu.com/api?v=2.0&ak={baidu_map_ak}',
            'baidu_map_script': 'https://api.map.baidu.com/getscript?v=2.0&ak={baidu_map_ak}'
        })
        self.assertEqual('https://api.map.baidu.com/api?v=2.0&ak=foo', manager.resolve_url('baidu_map_api'))


class CustomHostTestCase(unittest.TestCase):
    def test_add_host(self):
        m_context = {
            'echarts_version': '4.8.0'
        }

        manager = DependencyManager.create_default(
            context=m_context,
            repo_name='pyecharts'
        )
        manager.add_repo('demo', '/demo/')
        manager.add_repo('demo2', '/demo2/{echarts_version}')
        self.assertEqual(
            '/demo/fujian.js',
            manager.resolve_url('fujian', repo_name='demo')
        )
        self.assertEqual(
            '/demo2/4.8.0/fujian.js',
            manager.resolve_url('fujian', repo_name='demo2')
        )
