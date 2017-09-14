# django-echarts

![django-echarts version](https://img.shields.io/pypi/v/django-echarts.svg) ![python27](https://img.shields.io/badge/Python-2.7+-blue.svg) ![python35](https://img.shields.io/badge/Python-3.5+-blue.svg) ![django18](https://img.shields.io/badge/Django-1.8+-blue.svg)

基于 [chenjiandongx/pyecharts](https://github.com/chenjiandongx/pyecharts) 的 [Echarts](http://echarts.baidu.com/index.html)和 [Django](https://www.djangoproject.com) 的整合库。

> 目前该项目还处于开发状态(Alpha)，不建议在生产环境中使用。

## 概述

django-echarts提供了一系列用于整合的功能。主要有：

- 数据构建工具
- 基于前端或后端的数据渲染
- js静态文件管理
- 常用的命令工具

django-echarts使用到了Django常用部件，在使用之前应当对其有所了解。包括：

- 视图类(Class-Base View)
- 模板标签(Template Tag)
- 上下文处理器(Context Processor)
- 管理命令(Manage Command)

django-echarts支持Python2.7/3.5，需Django 1.8以上。

## 安装

可以从pypi安装

```
pip install django-echarts
```

或者使用源码构建

```
git clone https://github.com/kinegratii/django-echarts.git
cd django-echarts
python setup.py install
```

## 基本使用

1 添加 django_echarts包到项目配置模块的 `INSTALL_APPS`列表。

```python
INSTALL_APPS = (
    # Your apps
    'django_echarts'
    # Your apps
)
```

2 根据实际场景增加配置变量 `DJANGO_ECHARTS`，以重写某些设置项。

```python
DJANGO_ECHARTS = {
    'lib_js_host':'cdnjs'
}
```

或者全部采用默认值。

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

![Demo](images/demo1.gif)

## 开源协议

项目基于 MIT开源协议，欢迎提交 Issue & Pull request 。