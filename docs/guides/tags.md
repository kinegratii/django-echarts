# 模板标签库

## 导入

django-echarts 实现了与 pyecharts 功能上相似的模板标签，均定义在 `django_echarts.templatetags.echarts` 包。

> 模板基于DTE，而不是 jinja2。

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

## 标签库-echarts

### echarts_container

```python
django_echarts.templatetags.echarts.echarts_container(echarts_instance)
```
渲染图表容器(默认为 `<div></div>` )。

### echarts_js_dependencies

```python
django_echarts.templatetags.echarts.echarts_js_dependencies(*args)
```
渲染包含图表所需要的js文件的script一个或多个节点。

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

## 标签库-dje

### page_link

```
django_echarts.templatetags.dje.page_link(context, page_number)
```

