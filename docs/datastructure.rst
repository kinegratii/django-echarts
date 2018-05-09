数据结构
=========

多图表渲染
----------

.. versionadded:: 0.3.4

自 v0.3.4 新增 `django_echarts.datasets.charts.NamedCharts` 用于多图表渲染，该类是对于原有的 `pyecharts.custom.page.Page` 进行改善，包括：

- 增加图表对象命名引用
- 移除了 `list` 的相关方法

基本使用
++++++++


在创建一个 `NamedCharts` 实例 `charts` ，后，使用 `add_chart` 添加一个图表对象，可以使用 `name` 为之起一个引用名称，如果没有指定引用名称，则使用 c0,c1 命名。

::


    class MultipleChartsView(EChartsBackendView):
        echarts_instance_name = 'charts'
        template_name = 'multiple_charts.html'

        def get_echarts_instance(self, *args, **kwargs):
            device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
            device_types, counters = fetch(device_data, 'device_type', 'count')
            pie = Pie("设备分类", page_title='设备分类', width='100%')
            pie.add("设备分类", device_types, counters, is_label_show=True)

            battery_lifes = models.Device.objects.values('name', 'battery_life')
            names, lifes = fetch(battery_lifes, 'name', 'battery_life')
            bar = Bar('设备电量', page_title='设备电量', width='100%')
            bar.add("设备电量", names, lifes)
            charts = NamedCharts().add_chart(pie, name='pie').add_chart(bar)
            return charts

元素访问
++++++++

.. versionchanged:: 0.3.5
   图表访问方式从 *属性访问* 改为 *字典访问* 。

对于 包含若干图表的 `NamedCharts` 实例，可以像字典一样访问该图表对象。

Python 代码的访问方式

::

    # 访问 pie 对象 page_title
    print(charts['pie'].page_title)

    # 访问 bar 对象 page_title
    print(charts['c1'].page_title) # 推荐
    print(charts[1].page_title) # 不再推荐

模板代码的访问方式：

::

    {{ charts.pie.page_title }}
    {{ charts.c1.page_title }}

注意

::

    无论是 Jinja2 模板还是 Django 模板，均不提倡使用 `charts.1` 形式访问列表中的某一个元素。

NamedCharts VS Page
+++++++++++++++++++

`NamedCharts` 内部使用 `collections.OrderedDict` 保存图表名称和实例，支持字典访问方式，同时扩展原有的 `Page` 的列表特性。

具体差别如下表：

.. image:: /_static/namedcharts-vs-page.png
