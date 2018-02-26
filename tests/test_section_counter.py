# coding=utf8


import unittest
import random

from django_echarts.datasets.section_counter import BValueIndex, BRangeIndex, BSectionIndex, BSectionCounter


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


class BRangeCounterTestCase(unittest.TestCase):
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


class BSectionCounterTestCase(unittest.TestCase):
    def test_section_counter(self):
        rc = BSectionCounter(
            BValueIndex(0),
            BSectionIndex(1, 50),
            BSectionIndex(51, 99),
            BValueIndex(100)
        )
        test_data = [0, 12, 23, 34, 50, 60, 67, 99, 100]
        c = rc.feed(test_data)
        self.assertEqual(1, c['0'])
        self.assertEqual(4, c['1~50'])
        self.assertEqual(3, c['51~99'])
        self.assertEqual(1, c['100'])


class ComprehensiveTestCase(unittest.TestCase):
    def test_counter_with_section_indexes(self):
        source_data = [random.choice(range(1500)) for _ in range(2000)]

        # Test Using len Counter
        labels = ['00~00', '01~10', '11~50', '51~100', '101~500', '501~1000', '>1000']
        sizes = []
        sizes.append(len([pp for pp in source_data if pp == 0]))
        sizes.append(len([pp for pp in source_data if pp >= 1 and pp <= 10]))
        sizes.append(len([pp for pp in source_data if pp >= 11 and pp <= 50]))
        sizes.append(len([pp for pp in source_data if pp >= 51 and pp <= 100]))
        sizes.append(len([pp for pp in source_data if pp >= 101 and pp <= 500]))
        sizes.append(len([pp for pp in source_data if pp >= 501 and pp <= 1000]))
        sizes.append(len([pp for pp in source_data if pp >= 1001]))

        # Test Using section counter
        rc1 = BSectionCounter(
            BValueIndex(0),
            BSectionIndex(1, 10),
            BSectionIndex(11, 50),
            BSectionIndex(51, 100),
            BSectionIndex(101, 500),
            BSectionIndex(501, 1000),
            BSectionIndex(1001)
        )
        ls, cs = rc1.feed_as_axises(source_data)
        self.assertSequenceEqual(sizes, cs)
