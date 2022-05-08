# 组件存储类EntityFactory

本文对应于 `django_echarts.stores` 代码包。

## factory

全局变量，类型 `EntityFactory`。使用方式：

```python
from django_echarts.stores import factory

@factory.register_chart_widget
def my_bar():
    bar = Bar()
    # ...
    return bar

bar1 = factory.get_chart_widget('my_bar')
```

## EntityFactory

`EntityFactory` 是存储echarts图表创建器或者具体组件实例对象的容器。

### html_widgets

属性，类型 : `LazyDict`。组件创建器或实例存储。

### chart_widgets

属性，类型 : `LazyDict`。图表创建器或实例存储。

### chart_info_manager

属性，类型: `ChartInfoManagerMixin`。 存储图表关联的 `ChartInfo` 数据类。

### register_chart_widget

方法，可用作装饰器。注册图表创建器或实例。

### register_html_widget

方法，可用作装饰器。注册HTML组件创建器或实例。

### register_chart_info

方法。关联已有的 `ChartInfo`。

### get_chart_and_info

方法。获取给定name对应的图表实例和关联的 ChartInfo 。

### get_chart_widget

方法。返回对应name的图表实例。

### get_html_widget

方法。返回对应name的HTML组件实例。

### get_widget_by_name

方法。返回对应name的图表或HTML组件实例。

```python
chart1 = factory.get_widget_by_name('bar1')

info = factory.get_widget_by_name('info:bar1')
```



