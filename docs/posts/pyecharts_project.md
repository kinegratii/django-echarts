# pyecharts项目

> 本文介绍了pyecharts项目中与django-echarts相关的逻辑和django-echarts对其适配扩展的原理和实现。

> 本文以 pyecharts1.9和2.0为例。

## 图表支持

### 图表类型支持

pyecharts 的图表类体系如下：

```
- ChartMixin
  |- Base
  |- CompositeMixin
    |- Page
    |- Tab
  |- Table
  |- Image
```



django-echarts对图表类型支持情况如下：

- 仅支持所有继承自 `pyecharts.charts.base.Base` 的图表类型，即使用一个echarts即可定义的图表，包括 `Grid` 和 `Timeline`。
- 对于涉及到布局的 `CompositeMixin` ，django-echarts 提供了 `RowContainer` 、`Container` 等布局容器类。
- 可直接支持 `pyecharts.components.Table`，但更推荐直接使用 `prettytable.PrettyTable`。

代码实现方面，在 `render_widget` 时也直接引用该类。

```python
@render_widget.register(Base)
def render_chart(widget, **kwargs) -> SafeString:
    pass

@render_widget.register(Table)
@render_widget.register(PrettyTable)
def render_table(widget, **kwargs) -> SafeString:
    pass
```

### 图表属性和方法

图表属性和方法包括三个部分：

- 图表选项Opts：完全支持
- 依赖项js_dependencies：兼容性支持，直接使用 `list` 类型并允许项重复。依赖项去重工作在模板渲染前（调用模板函数）完成，这更加适用于同一页面有多个图表的情况。
- geojson地图：不支持pyecharts的内联引用方式。django-echarts提供了另一种外链引用方式。

`django_echarts.entities.chart_widgets.BlankChart` 是与 `Base` 相对应的接口类，通过比较二者的区别可以看出 django-echarts的改造扩展。

## 图表渲染

django-echarts 采用 Django Template Engine 而不是 Jinja2 ，因此模板函数/标签、模板tpl文件全部重写。

模板函数有三个，均定义在 `echarts` 模块。

```html
{% load echarts %}

{% dw_widget chart_obj %}
{% echarts_js_dependencies chart_obj %}
{% echarts_js_content chart_obj %}
```

其中后两个对标于 pyecharts的macro 函数。

| django-echarts模板函数               | pyecharts Jinja2 Macro           | 说明           |
| ------------------------------------ | -------------------------------- | -------------- |
| echarts_js_dependencies(*chart_list) | render_chart_dependencies(chart) | 渲染依赖项     |
| echarts_js_content(*chart_list)      | render_chart_content(chart)      | 渲染初始化脚本 |

与pyecharts不同的是，django-echarts的模板支持所有在 `django_echarts.renders` 注册的类，不仅包括图表类，也包括普通的HTML组件和容器组件。

代码实现方面，主要依赖于被 `singledispatch` 装饰的 `flat_chart` 函数。

模板文件定义在 *django_echarts/templates/snippets/echarts_init_options.tpl* 文件中，该文件使用 Django模板语法。

## 依赖项静态资源引用

主要功能：确定确定所使用的静态文件仓库。根据依赖项确定对应的url路径。

django-echarts的改造如下：

- 新增支持混合仓库。比如同一图表的 *echarts.min.js* 使用公共CDN文件，地图文件 *china.js* 使用本地文件（自行创建或远程下载）。
- 所有配置项均定义在 `settings.DJANGO_ECHARTS` 字典。

依赖项功能基本逻辑。

```
dep_name(依赖项名称)   --> filename(文件路径)  --> 引用URL/本地文件路径
```



## 自定义地图（geojson&svg）

pyecharts按内嵌方式引入geojson/svg数据，而 django-echarts 只支持 外链方式，这是二者最大的区别。详情参见 [《自定义地图》](/guides/custom_maps) 。

## 相关API接口

### 引用的类和接口

下列类和接口在 django-echarts 被直接引用。

- `pyecharts.charts.base.Base`
- `pyecharts.datasets.FILENAMES`
- `pyecharts.dataset.EXTRA`
- `pyecharts._version.__version__`
- `pyecharts.components.table.Table`
- `from pyecharts.globals.ThemeType`

### 无效的类和接口

以下类和方法函数在django-echarts不起作用。

- `pyecharts.globals.CurrentConfig`
- `pyecharts.charts.basic_charts.Map.add_geo_json`
- `pyecharts.charts.basic_charts.Geo.add_geo_json`
