# coding=utf8
"""
Test Cases for MCharts
"""

import sys
import unittest

from django_echarts.datasets.charts import MCharts

PY36 = sys.version_info[:2] >= (3, 6)


class MockChart:
    def __init__(self, page_title):
        self.page_title = page_title


class MChartsTestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        mc = MCharts().add_chart(
            MockChart('Line Chart'), name='line'
        ).add_chart(
            MockChart('Bar Chart')
        ).add_chart(
            MockChart('Map Chart'), name='map'
        )
        self.assertEqual('Line Chart', mc.line.page_title)
        self.assertEqual('Bar Chart', mc.c1.page_title)
        self.assertListEqual(
            ['Line Chart', 'Bar Chart', 'Map Chart'],
            [c.page_title for c in mc]
        )


@unittest.skipUnless(PY36, 'Order-retained dictionary is not supported')
class MChartsPY36TestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        mc = MCharts(
            bar=MockChart('Bar Chart'),
            line=MockChart('Line Chart')
        )
        mc.add_chart(MockChart('Map Chart'), name='map')
        self.assertEqual('Bar Chart', mc.bar.page_title)
        self.assertListEqual(
            ['Line Chart', 'Bar Chart', 'Map Chart'],
            [c.page_title for c in mc]
        )
