.. django_echarts documentation master file, created by
   sphinx-quickstart on Wed Dec  6 21:01:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django_echarts's documentation!
==========================================

django-echarts 是一个关于 Echarts_ 整合的 Django App，使用 pyecharts_ 作为图表构建库。主页： https://github.com/kinegratii/django-echarts

::

    自v0.3起，django-echarts 仅支持 Python3.5+ 的开发环境, Django 版本要求为 2.0+ 或 1.11 LTS 。

它提供了以下特性：

.. _Echarts: http://echarts.baidu.com/index.html
.. _pyecharts: https://github.com/chenjiandongx/pyecharts

- 基于前端/后端渲染方式的视图类
- 独立js依赖文件管理，支持多仓库自由切换
- 数据构建工具函数库
- 基于Django命令的CLI工具

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   tutorial
   topics
   data_builder
   fetch
   api
   development
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
