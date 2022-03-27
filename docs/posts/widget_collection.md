# 图表合辑

## 图表合辑

### 定义合辑

> class WidgetCollection(name: str, title: str = None, layout: Union[str, LayoutOpts] = 'a')

一个合辑对象 `WidgetCollection` 表示由若干图表和组件按照一定的布局组成的页面实体，继承 `Container`类。

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
>                        row_no: int = 0)
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
| ----------------------------- | ------------------------------------------------------- |
| l8                            | 每行显示1个图表，图表全部靠左显示                       |
| r8                            | 每行显示1个图表，图表全部靠右显示                       |
| s8                            | 每行显示1个图表，左右信息卡交叉显示                     |
| f6                            | 每行显示2个图表，不显示信息卡                           |
| f12                           | 每行显示1个图表，不显示信息卡                           |
| t6                            | 每行显示2个图表，信息卡显示在顶部。(信息卡包含少量文字) |
| b6                            | 每行显示2个图表，信息卡显示在低部。(信息卡包含大量文字) |

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

