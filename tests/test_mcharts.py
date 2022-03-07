# coding=utf8
"""
Test Cases for NamedCharts
"""

import sys
import unittest
from unittest.mock import MagicMock

from django_echarts.entities import NamedCharts


class MChartsTestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        nc = NamedCharts().add_chart(
            MagicMock(page_title='Line-Chart'), name='line'
        ).add_chart(
            MagicMock(page_title='Bar-Chart')
        ).add_chart(
            MagicMock(page_title='Map-Chart'), name='map'
        )
        self.assertEqual('Line-Chart', nc['line'].page_title)
        self.assertEqual('Bar-Chart', nc['c1'].page_title)
        self.assertListEqual(
            ['Line-Chart', 'Bar-Chart', 'Map-Chart'],
            [c.page_title for c in nc]
        )
        with self.assertRaises(KeyError):
            c = nc['no_charts']
            print(c.page_title)
        self.assertEqual('Bar-Chart', nc[1].page_title)


class MChartsPY36TestCase(unittest.TestCase):
    def test_create_with_kwargs(self):
        nc = NamedCharts(
            bar=MagicMock(page_title='Bar-Chart'),
            line=MagicMock(page_title='Line-Chart')
        )
        nc.add_chart(MagicMock(page_title='Map-Chart'), name='map')
        self.assertEqual('Bar-Chart', nc['bar'].page_title)
        self.assertListEqual(
            ['Bar-Chart', 'Line-Chart', 'Map-Chart'],
            [c.page_title for c in nc]
        )
