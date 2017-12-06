开发文档
=========

背景
-----

pyecharts 是一个优秀的 Echarts 的 Python 接口库，不仅实现了众多的图表类型，还支持在不同环境下（如纯Python、Jupyter Notebook以及web框架）运行。

pyecharts 默认使用 Jinja2 作为其模板引擎，并不适合直接与 Django 框架进行结合。基于此，本人开发 django-echarts 这个项目。

django-echarts使用到了Django 常用部件，在使用之前应当对其有所了解。包括：

- 项目配置(Settings)
- 视图类(Class-Based View)
- 模板标签(Template Tag)
- 上下文处理器(Context Processor)
- 管理命令(Manage Command)

开发原则
---------

由于 web环境和django框架的独有特性和开发规范，对于 pyecharts 作了一定的改造，pyecharts 某些功能并不适用于 django-echarts 。

配置
++++++

django-echarts 遵循统一配置的原则，所有的配置均定义在 `settings.DJANGO_ECHARTS` 常量中。


- `pyecharts.base.Base.jshost` 和 `pyecharts.custom.page.Page.jshost` 两个属性无效，应当在 `settings.DJANGO_ECHARTS` 中统一配置、

js引入方式
+++++++++++

js引入方式只支持外部链接方式


- 模板标签 `echarts_js-dependencies` 输出外部链接的 `<script>` 标签
- pyecharts 中 `echarts_js_dependencies_embed`  无对应的模板标签



其他
------

这里描述了这里描述了一些存在的隐藏性问题，这些问题不会影响功能上的运行，但可能对性能上有一定影响。

- jinja2 必须安装，即使是在 django 中使用自带的模板引擎