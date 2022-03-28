# 图表合辑

## 概述

合辑类 `WidgetCollection` 实现的是按照用户指定的布局填充相应的组件。

```
                   Container       WidgetGetterMixin
                      ^                   ^
                      |                   |
                      |                   |
user_layout --> WidgetCollection    EntityFactory
                      |
                      |- auto_mount(widget_container: WidgetGetterMixin)
```

这样可以减少中间环节的大量 `add_widget` 操作。比如，使用Container构建组件时：

```python
factory = EntityFactory()

container = Container()
row_container = RowContainer()
chart1, info, _ = factory.get_chart_and_info('my_chart_name')
row_container.add_widget(chart1, span=8)
row_container.add_widget(info)
container.add_widget(row_container)
```

使用 WidgetCollection 时，将中间 `RowContainer` 的创建和添加组件封装实现在 `auto_mount` 函数之中。

```python
factory = EntityFactory()

wc = WidgetCollection()
wc.add_chart_widget('my_chart_name', layout='l8')
wc.auto_mount(factory)
```



## 定义

> class WidgetCollection(name: str, title: str = None, layout: Union[str, LayoutOpts] = 'a')

一个合辑对象 `WidgetCollection` ，继承 `Container`类。

```python
wc = WidgetCollection(
    name='first_collection', title='第一个合辑', layout='s8'
)
```

参数列表

| 参数   | 类型 | 描述                                   |
| ------ | ---- | -------------------------------------- |
| name   | slug | 合辑标识符，作为url的一部分            |
| title  | str  | 标题，菜单栏的文字                     |
| layout | str  | 整体布局，仅对 `add_chart_widget` 方式 |

## 添加子组件

本节的添加方式均是按照 `auto_mount` 方式。

### 添加echarts图表

> WidgetCollection.add_chart_widget(self, chart_name: str, layout: str = 'l8')

`WdidgetCollection` 提供了 `pack_*` 方法用于添加组件，函数将参数的组件使用 `row` 类（一行12列）进行包裹。

```python
# 添加名为my_first的图表和对应的信息卡组件，以8:4方式显示
wc.add_chart_widget(chart_name='my_first', layout='l8')

# 显示名为my_named_charts的多图表组件NamedCharts。
wc.add_chart_widget(chart_name='my_named_charts', layout='l6')
```

### 添加HTML组件

>  WidgetCollection.add_html_widget(widget_list: List, spans:List=None)

构建一个 RowContainer 容器，并添加一个或多个子组件。

```python
# 按照给定的列数显示多个组件
wc.add_html_widget(widget_names=['w1', 'w2'], spans=[8, 4])
```



### 组件布局

添加不同组件可使用的布局不同。

| 布局layout |         | 合辑定义         | 只添加echarts图表 | 添加html组件     |
| ---------- | ------- | ---------------- | ----------------- | ---------------- |
| 类型       | 示例    | WidgetCollection | add_chart_widget  | add_html_widget  |
| str        | l8      | Y                | 8列图表 + 4列卡片 | -                |
|            | r8      | Y                | 4列卡片 + 8列图表 | -                |
|            | s8      | Y                | 交叉使用l8和r8    | -                |
| int        | 0       | -                | 12列图表          | 每个子组件平均分 |
|            | 8       | -                | 8列图表           | 每个子组件8列    |
| List[int]  | [4,4,4] | -                | 接受长度为2的列表 | Y                |



## 注册合辑

可以通过 `DJESite.register_collection` 方法构建一个图表合辑页面。

```python
site_obj = DJESite(site_title='DJE Demo')

@site_obj.register_chart(name='fj_fimily_type', title='示例图表1', layout='l8')
def fj_fimily_type():
    line = Line()
    # ...
    return line

@site_obj.register_chart(name='fj_area_bar', title='示例图表2', layout='l8')
def fj_fimily_type():
    bar = Bar()
    # ...
    return bar


@site_obj.register_collection
def collection1():
    wc = WidgetCollection(title='合辑01', layout='s8')
    wc.add_chart_widget(name='fj_area_bar')
    wc.add_chart_widget(name='fj_fimily_types')
    return wc
```

访问URL */collection/collection1/* 可以预览页面效果。

register_collection 函数参数及其意义：

| 参数            | 类型      | 说明                                      |
| --------------- | --------- | ----------------------------------------- |
| name            | slug      | 合辑标识，用于 `DJESite` 创建对应视图路由 |
| charts          | List[str] | 包含的图表标识                            |
| layout          | str       | 合辑布局                                  |
| title           | str       | 标题                                      |
| catalog         | str       | 如果设置，将添加合辑链接到该菜单项之下    |
| after_separator | bool      | 是否在菜单项前使用分隔符                  |

