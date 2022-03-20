# 模板标签库

## 导入

django-echarts 实现了与 pyecharts 功能上相似的模板标签，均定义在 `django_echarts.templatetags.echarts` 包。

在使用之前需要先行导入，有两种方式。

- 在每个模板文件使用 `{% laod echarts %}` 导入。
- 添加标签目录到项目配置项 `TEMPLATES.OPTIONS.libraries` ，这样就无需在每个模板都使用 load 标签。

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'echarts': 'django_echarts.templatetags.echarts'
            }
        },
    },
]
```

## 组件渲染

### 标签一览表

下表列出了各种组件对应的标签函数：

| 组件                      | 渲染标签                                    | kwargs参数             | 后端渲染js_init    |
| ------------------------- | ------------------------------------------- | ---------------------- | ------------------ |
| **单一组件**              |                                             |                        |                    |
| pycharts.charts.base.Base | dw_widget <sup>1</sup > / echarts_container | width / height         | echarts_js_content |
| prettytable.PrettlyTable  | dw_widget /   dw_table                      |                        | X                  |
| pycharts.charts.Table     | dw_widget /   dw_table                      |                        | X                  |
| ValuesPanel               | dw_widget /   dw_values_panel               | theme <sup>2</sup>     | X                  |
| Copyright                 | dw_widget                                   | theme                  | X                  |
| ChartInfo                 |                                             | theme                  |                    |
| NamedCharts               | dw_widget /   echarts_container             | theme / width / height | echarts_js_content |
| LinkItem / Menu           | dw_widget                                   | context / class_       |                    |
| Collection                | dw_widget /   echarts_container             |                        | echarts_js_content |

1. `dw_widget` 支持所有组件，`dw_table` / `dw_values_panel` / `echarts_container` 不再推荐使用。
2.  使用者无需传入`theme` 参数，引用自 `DJANGO_ECHARTS_SETTINGS.theme`。

### dw_widget

```python
# 标签函数
dw_widget(context, widget, **kwargs)
# 实际渲染函数
render_widget(widget, context, **kwargs)
```

使用方式如下：

```text
{% dw_widget chart %}
{% dw_widget chart  width="100%" height="700px" %}
```

可支持的参数：

| 参数   | 类型                   | 描述       |
| ------ | ---------------------- | ---------- |
| width  | Union[int, float, str] | 宽度       |
| height | Union[int, float, str] | 高度       |
| class_ | str                    | html元素类 |

### echarts_container

渲染图表，已被 `dw_widget` 替代。

## echarts初始化

### echarts_js_dependencies

```python
django_echarts.templatetags.echarts.echarts_js_dependencies(*args)
```
渲染包含图表所需要的js文件的script一个或多个节点。该函数会对args里面的图表依赖项进行汇总去重。

### echarts_js_content

```python
django_echarts.templatetags.echarts.echarts_js_content(*echarts_list)
```
渲染图表初始js代码，支持多图表。包含首尾的 `<script></script>` 标签。

### echarts_js_content_wrap

```python
django_echarts.templatetags.echarts.echarts_js_content_wrap(*echarts_list)
```

渲染图表初始js代码，支持多图表。不包含首尾的 `<script></script>` 标签。

### page_link

```
django_echarts.templatetags.dje.page_link(context, page_number)
```

## 主题相关

### theme_css

```python
django_echarts.templatetags.dje.theme_css()
```

渲染主题css。

### theme_js

```python
django_echarts.templatetags.dje.theme_js()
```

渲染主题javascript。

