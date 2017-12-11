# coding=utf8

from __future__ import unicode_literals

from pyecharts import Bar
from pluck import pluck

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56},
]

names, ages = zip(*pluck(objects, 'name', 'age'))

bar = Bar()
bar.add('The Age of Members', names, ages)

bar.render()
