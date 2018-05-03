# coding=utf8
"""
Test Cases for NamedCharts
"""

import sys
import unittest

from django_echarts.datasets.charts import NamedCharts

PY36 = sys.version_info[:2] >= (3, 6)


class MockChart:
    def __init__(self, page_title):
        self.page_title = page_title


class MChartsTestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        nc = NamedCharts().add_chart(
            MockChart('Line Chart'), name='line'
        ).add_chart(
            MockChart('Bar Chart')
        ).add_chart(
            MockChart('Map Chart'), name='map'
        )
        self.assertEqual('Line Chart', nc['line'].page_title)
        self.assertEqual('Bar Chart', nc['c1'].page_title)
        self.assertListEqual(
            ['Line Chart', 'Bar Chart', 'Map Chart'],
            [c.page_title for c in nc]
        )
        with self.assertRaises(KeyError):
            c = nc['no_charts']
            print(c.page_title)
        self.assertEqual('Bar Chart', nc[1].page_title)


@unittest.skipUnless(PY36, 'Order-retained dictionary is not supported')
class MChartsPY36TestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        nc = NamedCharts(
            bar=MockChart('Bar Chart'),
            line=MockChart('Line Chart')
        )
        nc.add_chart(MockChart('Map Chart'), name='map')
        self.assertEqual('Bar Chart', nc['bar'].page_title)
        self.assertListEqual(
            ['Bar Chart', 'Line Chart', 'Map Chart'],
            [c.page_title for c in nc]
        )
