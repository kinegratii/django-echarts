# 模板标签库

## 导入

django-echarts 实现了与 pyecharts 功能上相似的模板标签，均定义在 `django_echarts.templatetags.echarts` 包。在使用之前需要先行导入，有两种方式。

**方式一. 按需导入**

在每个需要使用标签函数的模板文件使用 `{% load echarts %}` 导入。

**方式二. 统一导入**

添加标签目录到项目配置项 `TEMPLATES.OPTIONS.libraries` ，这样就无需在每个模板都使用 load 标签。

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

### dw_widget

```python
django_echarts.templatetags.echarts.dw_widget(context, widget, **kwargs)
```

渲染单个组件，可以是图表组件、HTML组件和容器组件。使用方法如下：

```html
{% dw_widget row_container %}
{% dw_widget chart width="100%" height="700px" %}
```

可支持的参数：

| 参数   | 类型                   | 描述                                                         |
| ------ | ---------------------- | ------------------------------------------------------------ |
| width  | Union[int, float, str] | 宽度，仅适用于 pyecharts.charts.Base                         |
| height | Union[int, float, str] | 高度，仅适用于 pyecharts.charts.Base                         |
| class_ | str                    | 仅适用于LinkItem/Menu                                        |
| tpl    | str                    | 模板文件，仅适用于 HTMLBase。默认为 *widgets/{widget_name}.html* |

当widget为None（不包括0, ''等空值），`dw_widget` 将输出空字符串。

```html
# 直接使用即可
{% dw_widget widget %}

# 而不必使用if判断
{% if widget %}
  {% dw_widget widget %}
{% endif %}
```

### echarts_container

渲染图表，已被 `dw_widget` 替代。

## echarts初始化

> 本节标签函数中参数 widgets 参数传入任何组件对象，标签函数自动提取其中的echarts图表对象。

### echarts_js_dependencies

```python
django_echarts.templatetags.echarts.echarts_js_dependencies(*widgets)
```
渲染包含图表所需要的js文件的script一个或多个节点。该函数会对args里面的图表依赖项进行汇总去重。

在同一页面，应当保证 `echarts_js_dependencies` 只使用一次，避免部分库文件重复加载。

### echarts_js_content

```python
django_echarts.templatetags.echarts.echarts_js_content(*widgets)
```
渲染图表初始js代码，支持多图表。包含首尾的 `<script></script>` 标签。

### echarts_js_content_wrap

```python
django_echarts.templatetags.echarts.echarts_js_content_wrap(*widgets)
```

渲染图表初始js代码，支持多图表。不包含首尾的 `<script></script>` 标签。

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

## 其他

### page_link

```python
django_echarts.templatetags.dje.page_link(context, page_number)
```

将当前url增加page参数。

