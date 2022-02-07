# 详情页面（Detail）

## 新增图表

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
@site_obj.register_chart(description='词云示例', catalog='示例一')
def mychart():
    bar = Bar()
    # ...
    return bar
```



## 模板API

根据是否存在对应的图表，显示不同的模板。

| 特性   | 模板                | 变量名称  | 类型                   | 说明                                     |
| ------ | ------------------- | --------- | ---------------------- | ---------------------------------------- |
| 有图表 | {theme}/detail.html | menu      | `List[DJEChartInfo]`   | 图表的基本信息，包括标题、标识、介绍文本 |
|        |                     | chart_obj | `pycharts.charts.Base` | 图表对象。                               |
| 无图表 | {theme}/empty.html  | -         | -                      | -                                        |

## 