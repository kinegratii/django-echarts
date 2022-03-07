# coding=utf8

import unittest

from unittest.mock import MagicMock

from django_echarts.entities.chart_widgets import merge_js_dependencies


class MockCharts(object):
    """
    A mock class for pyecharts.base.Base and pyecharts.custom.page.Page.
    """

    def __init__(self, js_dependencies):
        self.js_dependencies = MagicMock(items=js_dependencies)


class JsMergeTestCase(unittest.TestCase):
    BASE_CHART = MockCharts(['echarts'])
    MAP_CHART = MockCharts(['echarts', 'fujian'])
    THREE_D_CHART = MockCharts(['echarts', 'echartsgl'])

    def test_one_chart_or_page(self):
        # One chart or one page
        self.assertListEqual(
            ['echarts'],
            merge_js_dependencies(self.BASE_CHART)
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies(self.MAP_CHART)
        )

    def test_multiple_charts_and_pages(self):
        # Multiple charts
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies(
                self.BASE_CHART,
                self.MAP_CHART
            )
        )
        self.assertListEqual(
            ['echarts', 'echartsgl'],
            merge_js_dependencies(self.BASE_CHART, self.THREE_D_CHART)
        )
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian'],
            merge_js_dependencies(self.MAP_CHART, self.THREE_D_CHART)
        )
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian'],
            merge_js_dependencies(self.BASE_CHART, self.MAP_CHART, self.THREE_D_CHART)
        )

    def test_string_dependencies(self):
        self.assertListEqual(
            ['echarts', 'echartsgl'],
            merge_js_dependencies('echartsgl', self.BASE_CHART)
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            merge_js_dependencies('echarts', ['echarts', 'fujian'])
        )

    def test_nested_js_dependencies(self):
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian'],
            merge_js_dependencies(
                merge_js_dependencies(self.BASE_CHART), self.MAP_CHART, self.THREE_D_CHART
            )
        )
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian', 'zhejiang'],
            merge_js_dependencies(
                merge_js_dependencies(self.BASE_CHART, self.MAP_CHART),
                self.THREE_D_CHART,
                'zhejiang'
            )
        )
