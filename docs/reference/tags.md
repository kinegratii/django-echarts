# 模板标签库

## 导入

django-echarts 实现了与 pyecharts 功能上相似的模板标签，均定义在 `django_echarts.templatetags.echarts` 包。在使用之前需要先行导入，有两种方式。

**1. 按需导入**

在每个需要使用标签函数的模板文件使用 `{% laod echarts %}` 导入。

**2. 统一导入**

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

> 本节标签函数中参数widgets参数指的是echarts图表对象组成的列表。

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

