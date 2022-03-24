# 组件和布局

## 组件

### 组件体系

django-echarts 定义了一套较为完整、可扩展的组件体系，主要组件包括：

| 组件                                   | 描述        | 渲染                               |                            |
| -------------------------------------- | ----------- | ---------------------------------- | -------------------------- |
|                                        |             | **函数dw_widget参数 <sup>1</sup>** | **模板文件**               |
| **echarts图表** <sup>2</sup>           |             |                                    |                            |
| pycharts.charts.base.Base <sup>3</sup> | echarts图表 | width / height                     | -                          |
| prettytable.PrettlyTable               | 表格        |                                    | -                          |
| pycharts.charts.Table                  | 表格        |                                    | -                          |
| **HTML组件**                           |             |                                    |                            |
| ChartInfo                              | 信息卡      | theme                              | widgets/chart_info.html    |
| Copyright                              | 版权栏      | theme                              | -                          |
| LinkItem / Menu                        | 菜单项/链接 | context / class_                   | -                          |
| ValueItem                              | 数字卡片    |                                    | value_item.html            |
| **容器组件**                           |             |                                    |                            |
| RowContainer                           | 行容器      |                                    | widgets/row_container.html |
| NamedCharts                            | 多图表      |                                    | widgets/row_container.html |
| ValuesPanel                            | 数值面板    |                                    | widgets/row_container.html |
| Collection                             | 合辑        |                                    | -                          |

1. 渲染标签函数均使用 `dw_widget` ，原有的 echarts_container/dw_table等不再使用。
1. echarts图表可关联 `ChartInfo` 。HTML组件不可关联。
2. `pyecharts.charts.base.Base` 类的图表，主要包括 Bar、Line、Grid、TimeLine等。
4. 使用者无需传入`theme` 参数，引用自 `DJANGO_ECHARTS_SETTINGS.theme`。



### 模板渲染

在模板中所有组件均可使用 *dw_widget* 渲染。

```
{% dw_widget chart1 %}
{% dw_widget chart2 width="100%" %}
```

## 单组件

### 表格(PrettyTable)

> pyecharts.charts.Table
>
> prettytable.PrettyTable
>
> django_echarts.entities.table_css(border=False, borderless=False, striped=False, size=None)



```python
from pyecharts.charts import Table
from django_echarts.entities.html_widgets import table_css

table = Table()
fields = ['位次', '城市', 'GDP(万亿)', '同比增长(%)']
gdp2021 = [
    [1, '福州市', 11324.5, 8.4], [2, '泉州市', 11304.2, 8.1],
    [3, '厦门市', 7033.9, 8.1], [4, '漳州市', 5025.4, 7.7],
    [5, '宁德市', 3151.1, 13.3], [6, '龙岩市', 3081.8, 7.7],
    [7, '三明市', 2953.5, 5.8], [8, '莆田市', 2883, 6.4],
    [9, '南平市', 2117.6, 6.5]
]
table.add(
    fields, gdp2021,
    attributes={'class': table_css(border=True, striped=True)}
)
```

`table_css` 函数用于定义表格的样式。

| 参数       | bootstrap对应类     | 描述     |
| ---------- | ------------------- | -------- |
| border     | table-bordered      | 边框     |
| borderless | table-borderless    | 无边框   |
| striped    | table-striped       | 阴影交叉 |
| size       | table-sm / table-md | 大小     |



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

ValuesPanel(col_item_num: int = 1)
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
| col_item_num    | int                       | 每行多少个       |

例子：

```python
@site_obj.register_html_widget
def home1_panel():
    number_p = ValuesPanel()
    # 显示图表总个数
    number_p.add_widget(ValueItem(str(site_obj.chart_info_manager.count()), '图表总数', '个', catalog='danger'))
    number_p.add_widget(ValueItem('42142', '网站访问量', '人次'))
    return number_p
```

## 容器组件

### 容器接口(ContainerBase)

```text
ContainerBase
    |-- Container
        |-- WidgetCollection
    |-- RowContainer
        |-- NamedCharts
        |-- ValuesPanel
```

`ContainerBase` 是一个通用的容器基础类，一般直接使用其子类 `container` 或 `RowContainer`，成员属性如下：

| 属性      | 类型                 | 描述               | Container | RowContainer        |
| --------- | -------------------- | ------------------ | --------- | ------------------- |
| _widgets  | OrderedDict          | 子组件列表         | 可用      | 可用                |
| _layouts  | Dict[str, LayoutCfg] | 每个组件的布局参数 | 无效      | 有效                |
| div_class | str                  | HTML元素class值    | 可自定义  | 不可更改，默认为row |

`ContainerBase` 既是布局上的容器，也是数据结构上的容器。

| 方法、函数      | 描述                   |
| --------------- | ---------------------- |
| len(container)  | 子组件数量             |
| list[container] | 迭代遍历子组件         |
| container[3]    | 获取第3个子组件        |
| container['c3'] | 获取名称为'c3'的子组件 |

### 添加组件

> ContainerBase.add_widget(widget, name: str = None, width: str = "", height: str = "", span: int = 0)

add_widget函数接受下列参数：

| 参数 <sup>1</sup> | 类型 | 描述                                                         |
| ----------------- | ---- | ------------------------------------------------------------ |
| widget            | Any  | 所有在 `renders.render_widget` 注册的图表组件、HTML组件和容器，可嵌套。 |
| name              | str  | 名称，如不提供默认为 'c1'、‘c2’等格式                        |
| width             | str  | 组件宽度，默认将调整 `pyecharts.charts.Base`图表类为 '100%'。 |
| height            | str  | 组件高度。如有设置，优先使用此值，而不是 `widget.height`。   |
| span              | int  | 样式类 `col-md-{span} col-sm-12` ，默认span=0表示平均分配。  |
| offset            | int  | 如果大于0则添加 `col-md-offset-{offset}` 样式类              |
| first             | bool | 添加到最后还是前面，默认添加到后面。                         |

1. `Container` 类的 `add_widget` 仅支持widget / name / first 三个参数。

### 通用容器(Container)

> Container(*args, div_class: str = '', **kwargs)

通用容器，其元素样式须由使用者自行制定。`add_widget` 不支持。

```python
page_container = Container(div_class='container-fluid')
row1 = RowContainer()
row2 = RowContainer()
page_container.add_widget(row1)
page_container.add_widget(row2)
```

渲染后如下

```html
<div class="container-fluid">
    <div class="row">...</div>
    <div class="row">...</div>
</div>
```



### 行布局容器(RowContainer)

> RowContainer(*args, **kwargs)

`RowContainer` 用于表示 bootstrap/material 框架的row容器，一行有12列，支持嵌套。

```python
rc = RowContainer()
c1, _, _ = site.resolve_chart('search_word_cloud')
rc.add_widget(c1)

rc2 = RowContainer()
ni = ValueItem('8.0', '福建省2021年GDP增长率', '%', catalog='info')
rc2.add_widget(ni, span=12)
ni2 = ValueItem('42142', '网站访问量', '人次')
rc2.add_widget(ni2, span=12)
ni3 = ValueItem('89.00', '中国联通5G套餐费用', '元', catalog='success')
rc2.add_widget(ni3, span=12)

rc.add_widget(rc2)
c2, _, _ = site.resolve_chart('fj_total_population')
rc.add_widget(c2)
```

效果图

![row_container_demo](../images/row_container_demo.png)

### 布局

有三种设置布局的方法：

**方法一. 单独设置**

逻辑如下：

- 如果 `add_widget` 同时指定一个大于0的span值，则该组件占用span列；
- 其余 span等于0的组件平均占用剩下的空间；
- 特别的，如果 `add_widget` 均未指定任何 span ，即每个组件的span均为0，则按一行12列平均分布各组件。

如

```python
rc = RowContainer()
rc.add_widget(w1, span=5)

rc2 = RowContainer()
rc2.add_widget(n1, span=12)
rc2.add_widget(n2, span=12)
rc.add_widget(rc2, span=2)

rc.add_widget(w2, span=5)
```

则布局渲染如下

```html
<div class="row">
    <div class="col-md-5 col-sm-12">...</div>
    <div class="col-md-2 col-sm-12">
        <div class="row">
            <div class="col-md-12 col-sm-12">...</div>
            <div class="col-md-12 col-sm-12">...</div>
        </div>
    </div>
    <div class="col-md-5 col-sm-12">...</div>
</div>
```

**方法二. 统一设置**

在添加完所有组件后，调用 `set_spans` 设置。

```python
rc = RowContianer()
rc.add_widget(w1)
rc.add_widget(w2)

rc.set_spans([4, 8]) # 4列，8列
rc.set_spans(6) # 6列
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

