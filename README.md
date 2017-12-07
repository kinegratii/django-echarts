# django-echarts

![django-echarts version](https://img.shields.io/pypi/v/django-echarts.svg) ![Development](https://img.shields.io/badge/Development-Alpha-orange.svg) ![python27](https://img.shields.io/badge/Python-2.7+-blue.svg) ![python35](https://img.shields.io/badge/Python-3.5+-blue.svg) ![django18](https://img.shields.io/badge/Django-1.8+-blue.svg)


django-echarts 是一个 [Echarts](http://echarts.baidu.com/index.html) 整合的  [Django](https://www.djangoproject.com) App，使用 [chenjiandongx/pyecharts](https://github.com/chenjiandongx/pyecharts) 的作为图表构建库。

> 目前该项目还处于测试状态(Beta)，欢迎试用和提交 issue & PR 。

## 概述

django-echarts 主要提供了以下的内容：

- 基于前端或后端的数据渲染
- javascript静态文件管理和加载
- 数据构建工具函数库
- 基于Django命令的CLI工具

## 安装

django-echarts的安装要求为：

- Python2.7+或者3.5+
- Django 1.8+
- pyecharts 0.3.0+

可以从pypi安装

```shell
pip install django-echarts
```

或者使用源码构建

```shell
git clone https://github.com/kinegratii/django-echarts.git
cd django-echarts
python setup.py install
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
    'lib_js_host':'cdnjs'
}
```

或者全部采用默认值。

3 根据渲染方式（前端或者后端方式）编写视图类，模板页面和路由。

前端渲染方式

```python
def create_simple_bar():
    bar = Bar("我的第一个图表", "这里是副标题")
    bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
    return bar


class SimpleBarView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return create_simple_bar()
      
```

后端渲染方式

```python
 class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        return create_simple_bar()
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

- [English Document](docs/us-en/api.md)
- [中文文档](docs/zh-cn/api.md)

## 示例

示例项目请参考 example 文件夹。

```shell
cd example
python manage.py runserver 127.0.0.1:8000
```

访问本地地址： http://127.0.0.1:8000 ，示例运行结果

![Demo](docs/images/django-echarts-demo.gif)

## 开源协议

项目基于 MIT开源协议，欢迎提交 Issue & Pull request 。
