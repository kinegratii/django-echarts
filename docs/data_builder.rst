数据构建工具
============

本文叙述了一些常见的数据构建的工具库，这些并不是 django-echarts 核心库的一部分。

这些工具的目标可能在 numpy 和pandas 库也有更好的实现方式，因此这里的工具针对非数据分析领域的使用者。

数据拾取
--------

zip 函数
+++++++++

`pyecharts.base.Base.add` 函数通常要求数据是两个长度相等的列表。

如果原始数据是其他形式的字典或元组列表，pyecharts 和 django-echarts 提供了若干个可以数据构建和转化的函数，以适配图表的相关方法。

例如内置的 `zip` 函数，可将列表按元素键名分解成多个列表。


::

        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        # t_data = [(21, '2017-12-01'), (19, '2017-12-02'), (20, '2017-12-03')]
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)

fetch 函数
+++++++++++

自 v0.2.1 起，新增 `django_echarts.datasets.fetch.fetch` 函数，该函数是对原有 pluck + zip 函数的进一步封装。

如

::

    from pyecharts import Bar
    from django_echarts.datasets.fetch import fetch

    objects = [
        {'id': 282, 'name': 'Alice', 'age': 30},
        {'id': 217, 'name': 'Bob', 'age': 56},
        {'id': 328, 'name': 'Charlie', 'age': 56},
    ]

    names, ages = fetch(objects, 'name', 'age')

    bar = Bar()
    bar.add('The Age of Members', names, ages)

AxisValuesQuerySet 类
++++++++++++++++++++++++++

如果数据来源于数据库，还可以使用 `django_echarts.datasets.managers.AxisValuesQuerySet` 链式查询方法。

首先需要通过以下两种方式将 `AxisValuesQuerySet` 整合到自定义的 Manager 。

::

    class TemperatureRecord(models.Model):
        # ...fields
        objects = AxisValuesQuerySet.as_manager()
        # Another way
        # objects = models.Manager.from_queryset(AxisValuesQuerySet)()

就可以如下面的代码一样使用。

::

        hs, ds = models.TemperatureRecord.objects.all().order_by('create_time').as_axis_values('high', 'create_time')
        line = Line('High Temperature')
        line.add('High', ds, hs)


还可以配合 `values` 和 `values_list` 函数使用，以上查询也可以写成

values

::

        hs, ds = models.TemperatureRecord.objects.all().order_by('create_time').values('high', 'create_time').as_axis_values('high', 'create_time')
        line = Line('High Temperature')
        line.add('High', ds, hs)

values_list，需要确保 named=True ，否则应当使用内置的 zip 函数。

::

        hs, ds = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time', named=True).as_axis_values('high', 'create_time')
        line = Line('High Temperature')
        line.add('High', ds, hs)

计数工具库 BSectionCounter
------------------------------

BSectionCounter 库用于计算符合一系列条件的数目计数类。

先看一个例子

::

    data_list = list(df['stars'])
    labels = ['00~00', '01~10', '11~50', '51~100', '101~500', '501~1000', '>1000']
    sizes = []
    sizes.append(len([pp for pp in data_list if pp == 0]))
    sizes.append(len([pp for pp in data_list if pp >= 1 and pp <= 10]))
    sizes.append(len([pp for pp in data_list if pp >= 11 and pp <= 50]))
    sizes.append(len([pp for pp in data_list if pp >= 51 and pp <= 100]))
    sizes.append(len([pp for pp in data_list if pp >= 101 and pp <= 500]))
    sizes.append(len([pp for pp in data_list if pp >= 501 and pp <= 1000]))
    sizes.append(len([pp for pp in data_list if pp >= 1001]))
    stargazer_bar = Bar("stars", "stars hist graph of users", width=CHART_WIDTH)
    stargazer_bar.add("", labels, sizes, is_label_show=True, mark_line=["average"])

使用 BSelectionCounter 后，简化为

::

    data_list = list(df['stars'])
    rc1 = BSectionCounter(
        BValueIndex(0),
        BSectionIndex(1, 10),
        BSectionIndex(11, 50),
        BSectionIndex(51, 100),
        BSectionIndex(101, 500),
        BSectionIndex(501, 1000),
        BSectionIndex(1001)
    )
    labels, sizes = rc1.feed_as_axises(source_data)
    stargazer_bar = Bar("stars", "stars hist graph of users", width=CHART_WIDTH)
    stargazer_bar.add("", labels, sizes, is_label_show=True, mark_line=["average"])

Dataset库
----------

该库将基于 Echarts 4.0 新增的 Dataset 特性。

敬请期待。

关系图数据构建
------------------

对于复杂的关系图，可以使用 networkx_ 库构建节点和连线，并传递给 `add` 函数。

.. _networkx: https://github.com/networkx/networkx

*graph_demo.py*

.. literalinclude:: /codes/graph_demo.py

渲染后的关系图如下：

.. image:: /_static/networkx-graph-demo.png
