# coding=utf8

from __future__ import unicode_literals

import unittest

from django_echarts.datasets.section_counter import BValueIndex, BRangeIndex, BSectionCounter


class BRangeIndexTestCase(unittest.TestCase):
    def test_basic(self):
        ri = BRangeIndex(3, 7)
        self.assertFalse(2 in ri)
        self.assertTrue(5 in ri)
        self.assertEqual('3~7', str(ri))

        ri = BRangeIndex(2)
        self.assertTrue(2 in ri)
        self.assertTrue(1000 in ri)
        self.assertEqual('≥2', str(ri))

        ri = BRangeIndex(upper=23)
        self.assertTrue(22 in ri)
        self.assertFalse(23 in ri)
        self.assertEqual('<23', str(ri))


class BSectionCounterTestCase(unittest.TestCase):
    def test_value_indexes(self):
        rc = BSectionCounter(
            BValueIndex(1),
            BValueIndex(2),
            BValueIndex(3)
        )
        c = rc.feed([1, 2, 3, 1, 2, 3, 1, 2, 2, 3, 3, 3, 5, 6])
        self.assertEqual(3, c['1'])
        self.assertEqual(4, c['2'])
        self.assertEqual(5, c['3'])

    def test_basic_usage(self):
        rc = BSectionCounter(
            BRangeIndex(0, 50),
            BRangeIndex(50, 100),
            BRangeIndex(100)
        )
        c = rc.feed([0, 12, 23, 34, 50, 60, 67, 100])  # 4,3,1
        self.assertEqual(4, c['0~50'])
        self.assertEqual(3, c['50~100'])
        self.assertEqual(1, c['≥100'])

    def test_simple_counter(self):
        rc = BSectionCounter.from_simple([0, 50], [50, 100], [100, None])
        c = rc.feed([0, 12, 23, 34, 50, 60, 67, 100])  # 4,3,1
        self.assertEqual(4, c['0~50'])
        self.assertEqual(3, c['50~100'])
        self.assertEqual(1, c['≥100'])

    def test_feed_as_axis(self):
        rc = BSectionCounter.from_simple([0, 50], [50, 100], [100, None])
        a, b = rc.feed_as_axises([0, 12, 23, 34, 50, 60, 67, 100])  # 4,3,1
        self.assertTupleEqual(('0~50', '50~100', '≥100'), a)
        self.assertTupleEqual((4, 3, 1), b)

    def test_missing_index(self):
        rc = BSectionCounter(
            BRangeIndex(None, 0),
            BRangeIndex(0, 50),
            BRangeIndex(50, 100),
            BRangeIndex(100)
        )
        c = rc.feed([0, 12, 23, 34, 50, 60, 67, 100])  # 4,3,1
        self.assertEqual(0, c['<0'])
