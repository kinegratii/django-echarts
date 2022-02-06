# 详情页面（Detail）

## 构建pyecharts图表-FBV

`site_obj.register_chart` 装饰器用于注册返回图表的函数。

```python
@site_obj.register_chart
def mychart():
    bar = Bar()
    # ...
    return bar
```

默认未携带任何参数情况下，函数名将作为图表标识符。

当然也可以携带一些参数，这些参数通常和 `DJEChartInfo` 类参数意义相同。

```python
@site_obj.register_chart(description='词云示例', menu_text='示例一')
def mychart():
    bar = Bar()
    # ...
    return bar
```



## 构建pyecharts图表-CBV

类方式（Clased-base view）通常是将具有紧密意义的图表组成一组，在代码上以类方式体现。

```python
class MyDemoDetailView(DJESiteDetailView):
    charts_config = [('c1', '柱形图'), ('c2', '饼图')]

    def dje_chart_c1(self, *args, **kwargs):
        bar = Bar()
        # ...
        return bar

    def dje_chart_c2(self, *args, **kwargs):
        pie = Pie()
        # ...
        return pie


site_obj.register_detail_view(MyDemoDetailView, menu_text='示例一')
```

函数名称必须符合 `"dje_chart_<chart_name>"` 的格式要求。

## 模板API

根据是否存在对应的图表，显示不同的模板。

| 特性   | 模板                | 变量名称  | 类型                   | 说明                                     |
| ------ | ------------------- | --------- | ---------------------- | ---------------------------------------- |
| 有图表 | {theme}/detail.html | menu      | `List[DJEChartInfo]`   | 图表的基本信息，包括标题、标识、介绍文本 |
|        |                     | chart_obj | `pycharts.charts.Base` | 图表对象。                               |
| 无图表 | {theme}/empty.html  | -         | -                      | -                                        |

## 