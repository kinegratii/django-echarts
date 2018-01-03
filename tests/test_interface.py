# coding=utf8

from __future__ import unicode_literals

import unittest

from django_echarts.utils.interfaces import merge_js_dependencies


class MockCharts(object):
    def __init__(self, js_dependencies):
        self.js_dependencies = js_dependencies


class JsMergeTestCase(unittest.TestCase):
    def test_merge_js(self):
        self.assertEqual(
            ['echarts'],
            merge_js_dependencies(MockCharts(['echarts']))
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies('echarts', MockCharts(['echarts', 'fujian']))
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies('echarts', 'fujian')
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies('echarts', 'echarts', 'fujian')
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies('echarts', ['echarts', 'fujian'])
        )
