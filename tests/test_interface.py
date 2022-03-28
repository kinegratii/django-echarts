# coding=utf8

import unittest

from unittest.mock import MagicMock

from django_echarts.renders import get_js_dependencies, flat_chart


class MockCharts:
    """
    A mock class for pyecharts.base.Base and pyecharts.custom.page.Page.
    """

    def __init__(self, js_dependencies):
        self.js_dependencies = MagicMock(items=js_dependencies)


@flat_chart.register(MockCharts)
def flat_mock(widget):
    return [widget]


class JsMergeTestCase(unittest.TestCase):
    BASE_CHART = MockCharts(['echarts'])
    MAP_CHART = MockCharts(['echarts', 'fujian'])
    THREE_D_CHART = MockCharts(['echarts', 'echartsgl'])

    def test_one_chart_or_page(self):
        # One chart or one page
        self.assertListEqual(
            ['echarts'],
            get_js_dependencies(self.BASE_CHART)
        )
        self.assertListEqual(
            ['echarts', 'fujian'],
            get_js_dependencies(self.MAP_CHART)
        )

    def test_multiple_charts_and_pages(self):
        # Multiple charts
        self.assertListEqual(
            ['echarts', 'fujian'],
            get_js_dependencies([self.BASE_CHART, self.MAP_CHART])
        )
        self.assertListEqual(
            ['echarts', 'echartsgl'],
            get_js_dependencies([self.BASE_CHART, self.THREE_D_CHART])
        )
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian'],
            get_js_dependencies([self.MAP_CHART, self.THREE_D_CHART])
        )
        self.assertListEqual(
            ['echarts', 'echartsgl', 'fujian'],
            get_js_dependencies([self.BASE_CHART, self.MAP_CHART, self.THREE_D_CHART])
        )

    def test_string_dependencies(self):
        self.assertListEqual(
            ['echarts', 'echartsgl'],
            get_js_dependencies(['echartsgl', self.BASE_CHART])
        )
