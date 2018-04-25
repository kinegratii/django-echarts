# coding=utf8


import unittest

from django_echarts.datasets.fetch import fetch, fetch_single, ifetch_multiple

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
        names, ages = map(list, ifetch_multiple(DICT_LIST_DATA, 'name', 'age'))
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


class MockItem:
    def __init__(self, x, y, z):
        self._data = {'x': x, 'y': y, 'z': z}

    def get(self, key):
        return self._data.get(key)


class FetchCustomGetterTestCase(unittest.TestCase):
    def test_custom_getter(self):
        data_list = [MockItem(1, 2, 3), MockItem(4, 5, 6), MockItem(7, 8, 9)]
        xs, ys, zs = fetch(data_list, 'x', 'y', 'z', getter=lambda item, key: item.get(key))
        self.assertListEqual([1, 4, 7], xs)

    def test_with_dict(self):
        """
        Use dict.get(key) to pick item.
        """
        names, ages = fetch(DICT_LIST_DATA, 'name', 'age', getter=lambda item, key: item.get(key))
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])
