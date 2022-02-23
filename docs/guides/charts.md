# pyecharts图表开发

## 概述

django-echarts 的底层定位于 pyecharts 和 django 的整合库，主要代码位于 `django_echarts.core` 包。

在具体实现上对 pyecharts 的一些部分进行改造以适配 web 或 Django 环境。

| 模块           | 改造方法                                      |
| -------------- | --------------------------------------------- |
| 图表构建       | 90%以上可直接引用，部分不支持                 |
| 静态文件引用   | 扩展实现                                      |
| 模板引擎       | 使用DTS重新实现，便于与其他第三方库进行整合。 |
| web主题框架    | django-echarts新增                            |
| 静态文件下载器 | django-echarts新增                            |



## 图表类型

### 图表类型支持

目前 django-echarts不支持以下图表类型

- 表格 `pyecharts.components.Table`
- 选项页 `pyecharts.charts.Tab`
- 百度地图 `pyecharts.charts.BMap`
- 页面 `pyechars.charts.Page` 可以使用 `django_echarts.core.charttools.NamedCharts`

### NamedCharts

NamedCharts 和 Page 类似，能够同时显示多个图表，兼容内置的响应式布局。

```python
@site_obj.register_chart(name='named_charts', title='NamedCharts示例', description='使用NamedCharts')
def named_charts():
    page = NamedCharts(page_title='复合图表', col_num=2)
    pie = Pie()
    page.add_chart(pie, 'pie')
    
    bar = Bar()
    page.add_chart(bar, 'bar')
    return page
```

说明：

- col_num 表示每行的图表个数，推荐设置1-3即可。在小屏幕上将自动调整为每行一个。
- add_chart 函数将宽度设置为 100%。

## ECharts主题

```
DJEOpts.enable_echarts_theme:bool = False
```

django-echarts 支持 echarts 主题功能，为了减少主题资源加载，默认情况下不启用该功能。

- 全局配置：`enable_echarts_theme = False`
- 不会请求任何theme对应的javascript文件
- 前端 `echarts.init` 函数不传入任何主题参数，即使 python代码`pycharts.options.InitOpts` 传入了 `theme` 参数

