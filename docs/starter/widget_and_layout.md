# 组件和布局

## 组件

### 组件体系

django-echarts 定义了一套较为完整的组件体系，主要逐渐包括：

| 组件                                   | 描述        | 模板标签                        | 标签函数               |
| -------------------------------------- | ----------- | ------------------------------- | ---------------------- |
| **echarts图表** <sup>1</sup>           |             |                                 |                        |
| pycharts.charts.base.Base <sup>2</sup> | echarts图表 | dw_widget / echarts_container   | width / height         |
| prettytable.PrettlyTable               | 表格        | dw_widget /   dw_table          |                        |
| pycharts.charts.Table                  | 表格        | dw_widget /   dw_table          |                        |
| ChartInfo                              | 信息卡      |                                 | theme                  |
| NamedCharts                            | 多图表      | dw_widget /   echarts_container | theme / width / height |
| **HTML组件**                           |             |                                 |                        |
| ValuesPanel                            | 数值面板    | dw_widget /   dw_values_panel   | theme <sup>3</sup>     |
| Copyright                              | 版权栏      | dw_widget                       | theme                  |
| LinkItem / Menu                        | 菜单项/链接 | dw_widget                       | context / class_       |
| **容器组件**                           |             |                                 |                        |
| Collection                             | 合辑        | dw_widget /   echarts_container |                        |

1. echarts图表可关联 `ChartInfo` 。HTML组件不可关联。
2. `pyecharts.charts.base.Base` 类的图表，主要包括 Bar、Line、Grid、TimeLine等。
4. 使用者无需传入`theme` 参数，引用自 `DJANGO_ECHARTS_SETTINGS.theme`。



### 模板渲染

在模板中所有组件均可使用 *dw_widget* 渲染。

```
{% dw_widget chart1 %}
{% dw_widget chart2 width="100%" %}
```



## 组件API

### 多图表(NamedCharts)

> class NamedCharts(page_title: str = 'EChart', col_chart_num: int = 1, is_combine: bool = False)

NamedCharts 是一个多图表的图表类，能够同时显示多个图表，使用 add 函数添加图表对象。

```python
ncharts = NamedCharts(page_title='复合图表', col_num=2)
pie = Pie()
ncharts.add_chart(pie, 'pie')

bar = Bar()
ncharts.add_chart(bar, 'bar')

bar2 = Bar()
ncharts.add_chart(bar2) # 默认分配 'c{n}' 作为名称，此项为 'c2'
```

构造函数参数：

| 参数          | 类型 | 描述         |
| ------------- | ---- | ------------ |
| page_title    | str  | 标题         |
| col_chart_num | str  | 每行图表个数 |
| is_combine    | bool | 是否引用     |

**图表引用**

按字典方式引用某个图表。

python代码

```python
ncharts['pie'] # result: pie
ncharts[0] # result: pie
ncharts['c2'] # result: bar2
```

模板代码

```html
{% dw_widget ncharts.pie %}
{% dw_widget ncharts.c2 %}
```



### 数字仪盘(ValuesPanel)

```python
ValueItem(value: Any, description: str, unit: str = None, catalog: str = 'primary', trend: Literal['up', 'down', ''] = '')

ValuesPanel(data: List[ValueItem] = None, col_item_num: int = 1)
```

以突出方式显示数字数值。

| 参数            | 类型                      | 描述             |
| --------------- | ------------------------- | ---------------- |
| **ValueItem**   |                           |                  |
| value           | Any                       | 数值型数据       |
| description     | str                       | 描述性文字       |
| unit            | str                       | 单位文字         |
| catalog         | str                       | 决定背景颜色     |
| arrow           | Literal['up', 'down', ''] | 数字后的箭头符号 |
| **ValuesPanel** |                           |                  |
| data            | List[ValueItem]           | 数字项列表       |
| col_item_num    | int                       | 每行多少个       |

例子：

```python
@site_obj.register_html_widget
def home1_panel():
    number_p = ValuesPanel(col_item_num=4)
    # 显示图表总个数
    number_p.add(ValueItem(str(site_obj.chart_info_manager.count()), '图表总数', '个', catalog='danger'))
    number_p.add(ValueItem('42142', '网站访问量', '人次'))
    return number_p
```



## 图表合辑

### 定义合辑

> class WidgetCollection(name: str, title: str = None, layout: Union[str, LayoutOpts] = 'a')

一个合辑对象 `WidgetCollection` 表示由若干图表和组件按照一定的布局组成的页面实体。

```python
wc = WidgetCollection(
    name='first_collection', title='第一个合辑', layout='s8'
)
```

参数列表

| 参数   | 类型 | 描述                        |
| ------ | ---- | --------------------------- |
| name   | slug | 合辑标识符，作为url的一部分 |
| title  | str  | 标题，菜单栏的文字          |
| layout | str  | 整体布局                    |

### 添加组件

> WidgetCollection.pack_chart_widget(chart_obj, info: ChartInfo, ignore_ref: bool = True, layout: str = 'l8',
>                           row_no: int = 0)
>
>  
>
> WidgetCollection.pack_html_widget(widget_list: List, layout: str = 'f', row_no: int = 0)



`WdidgetCollection` 提供了 `pack_*` 方法用于添加组件，函数将参数的组件使用 `row` 类（一行12列）进行包裹。

```python
# 添加单个图表
bar = Bar()
info = DJEChartInfo(...)
wc.pack_chart_widget(bar, info, layout='l8')

# 多图表平均显示
nc = NamedCharts()
bar2 = Bar()
line = Line()
nc.add_chart(line1)
nc.add_chart(bar)
wc.pack_chart_widget(nc, layout='f6')

# 按照给定的列数显示多个组件
wc.pack_html_widget([w1, w2], [8, 4])
```

### 图表布局

布局分为网格布局和行内布局两种。布局方式使用一个字母和一个数字组成的字符串。第1个字母表示图表的所在位置，第2个字母表示图表所占用的列数（总列数为12）。可使用的位置标识（使用首字母即可）如下：

| 标识 | left | right | top  | bottom | full           | stripped     | auto           |
| ---- | ---- | ----- | ---- | ------ | -------------- | ------------ | -------------- |
| 描述 | 左侧 | 右侧  | 顶部 | 底部   | 不显示信息Info | 左右交叉图表 | 按行内布局显示 |

使用规则：

- 其中 a和s仅合辑网格布局可使用。
- lrtbf布局网格布局和行内布局均可使用。
- l8表示 “图表8列 + 信息卡4列”； r8 表示“信息卡4列+图表8列”
- 响应式布局：所设置的列数仅在md以上有效，sm及其以下均会扩展到整行12列

下面是常见使用场景的布局定义：

| WidgetWidgetCollection.layout | 描述                                                    |
| ---------------------------- | ------------------------------------------------------- |
| l8                           | 每行显示1个图表，图表全部靠左显示                       |
| r8                           | 每行显示1个图表，图表全部靠右显示                       |
| s8                           | 每行显示1个图表，左右信息卡交叉显示                     |
| f6                           | 每行显示2个图表，不显示信息卡                           |
| f12                          | 每行显示1个图表，不显示信息卡                           |
| t6                           | 每行显示2个图表，信息卡显示在顶部。(信息卡包含少量文字) |
| b6                           | 每行显示2个图表，信息卡显示在低部。(信息卡包含大量文字) |

### 注册合辑

可以通过 `rDJESite.register_collection` 方法构建一个图表合辑页面。

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

| 参数            | 类型      | 说明                                   |
| --------------- | --------- | -------------------------------------- |
| name            | slug      | 合辑标识                               |
| charts          | List[str] | 包含的图表标识                         |
| layout          | str       | 合辑布局                               |
| title           | str       | 标题                                   |
| catalog         | str       | 如果设置，将添加合辑链接到该菜单项之下 |
| after_separator | bool      | 是否在菜单项前使用分隔符               |

