# coding=utf8

from __future__ import unicode_literals

import pluck
import unittest
from django_echarts.plugins.fetch import fetch, fetch_single, ifetch_multiple

DICT_LIST_DATA = [
    {'id': 282, 'name': 'Alice', 'age': 30, 'sex': 'female'},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56, 'sex': 'male'},
]


class FetchTestCase(unittest.TestCase):
    def test_fetch_single(self):
        names = fetch_single(DICT_LIST_DATA, 'name')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        sexs = fetch_single(DICT_LIST_DATA, 'sex', default='male')
        self.assertListEqual(sexs, ['female', 'male', 'male'])

    def test_ifetch_multiple(self):
        names, ages = map(list, ifetch_multiple(DICT_LIST_DATA, {}, 'name', 'age'))
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])

    def test_fetch(self):
        names = fetch(DICT_LIST_DATA, 'name')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])

        sexs = fetch(DICT_LIST_DATA, 'sex', default='male')
        self.assertListEqual(sexs, ['female', 'male', 'male'])

        names, ages = fetch(DICT_LIST_DATA, 'name', 'age')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])

        names, ages, sexs = fetch(DICT_LIST_DATA, 'name', 'age', 'sex', defaults={'sex': 'male'})
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])
        self.assertListEqual(sexs, ['female', 'male', 'male'])
