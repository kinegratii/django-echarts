# django-echarts

![django-echarts version](https://img.shields.io/pypi/v/django-echarts.svg) [![Build Status](https://travis-ci.org/kinegratii/django-echarts.svg?branch=master)](https://travis-ci.org/kinegratii/django-echarts) ![PyPI - Status](https://img.shields.io/pypi/status/django-echarts.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-echarts.svg) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-echarts.svg)



django-echarts 是一个 [pyecharts](https://github.com/pyecharts/pyecharts) +  [Django](https://www.djangoproject.com) 整合的 Django App。

## 概述

django-echarts 主要提供了以下的内容：

- **“前端渲染”** / **后端渲染** 两种不同的渲染方式
- 基于 Django Template Engine 的模板标签库
- js/css静态文件托管
- 数据构建工具函数库
- 项目级的CLI工具

## 安装

### pyecharts

请根据你的 pyecharts 版本安装 django-echarts 。

| django-echarts版本系列 | pyecharts | django | python | 备注 |
| ------ | ------ | ------ | ----- | ----- |
| 0.3.x | 0.3.x - 0.4.x | 1.11/2.0 | 3.5 | 不再维护 |
| 0.5.x | 1.9+ | 2.0+ | 3.7+ | 开发中 |

### 安装方式

可以使用 pip 在线安装。

```shell
pip install django-echarts
```

## 快速使用

1 添加 django_echarts包到项目配置模块的 `INSTALL_APPS`列表。

```python
INSTALL_APPS = (
    # Your apps
    'django_echarts',
    # Your apps
)
```

2 根据实际场景需要设置一些配置参数，这些参数必须定义在项目模块中一个名为 `DJANGO_ECHARTS` 的字典里。

```python
DJANGO_ECHARTS = {
    'echarts_version': '4.0.4',
    'lib_js_host':'cdnjs'
}
```

由于不同 ECharts 版本会有一些功能和形式上的区别，建议自行指定某一个版本。

3 编写视图类，模板页面和路由。

```python

from pyecharts.charts import Bar
from pyecharts import options as opts
from django_echarts.views import EChartsBackendView

class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        bar = Bar().add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]).add_yaxis(
        '面积', [5, 20, 36, 10, 75, 90]
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="我的第一个图表", subtitle="单位：这里是副标题")
        )
        return bar
```

4 编写模板文件，可以使用相关标签（定义在`echarts`标签库里）渲染JS内容。

```html
{% extends 'base.html' %}
{% load echarts %}

{% block main_content %}
    <div class="row row-offcanvas row-offcanvas-right">
        <div class="col-xs-6 col-sm-2 sidebar-offcanvas" id="sidebar">
            <div class="list-group">
                <a href="?name=bar" class="list-group-item">柱形图(Bar)</a>
                <a href="?name=kine" class="list-group-item">K线图(KLine)</a>
                <a href="?name=map" class="list-group-item">地图(Map)</a>
                <a href="?name=pie" class="list-group-item">饼图(Pie)</a>
            </div>
        </div>
        <!--/.sidebar-offcanvas-->
        <div class="col-xs-12 col-sm-10">
            <p class="pull-right visible-xs">
                <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
            </p>
            {# 渲染容器 #}
            {% echarts_container echarts_instance %}

        </div>
        <!--/.col-xs-12.col-sm-9-->
    </div>

{% endblock %}

{% block extra_script %}
    {# 渲染依赖文件 #}
    {% echarts_js_dependencies echarts_instance %} 
    {# 渲染初始化文本 #}
    {% echarts_js_content echarts_instance %}
{% endblock %}
```

5 在部署到正式环境时，如果需要使用公共CDN托管常用JS文件，可修改项目配置，使得 `lib_js_host`或者`map_js_host`指向公共CDN。

## 文档

[在线文档](http://django-echarts.readthedocs.io/zh_CN/latest/index.html)

## 示例

示例项目位于 example 文件夹。

第一步，安装依赖

```shell
cd example
pip install -r requirements.txt
```

第二步，启动项目开发服务器

```shell
python manage.py runserver 127.0.0.1:8000
```

访问本地地址： http://127.0.0.1:8000 ，示例运行结果

![Demo](docs/images/django-echarts-demo.gif)

## 开源协议

项目基于 MIT开源协议，欢迎提交 Issue & Pull request 。
