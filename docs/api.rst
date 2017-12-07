API
=====

本文档描述了django-echarts项目的API信息。

视图(Views)
------------

视图是渲染逻辑的部件。

EChartsMixin
+++++++++++++

 `django_echarts.views.base.EChartsMixin` 

所有视图的接口类。

**get_echarts_instance**

 `get_echarts_instance(self, *args, **kwargs)` 

接口函数，此接口需要返回一个用于图表实例，通常是 `pyecharts.base.Base` 的子类实例。

EChartsFrontendView
++++++++++++++++++++

 `django_echarts.views.frontend.EChartsFrontendView` 

基于前端(ajax)的渲染视图类。

EChartsBackendView
+++++++++++++++++++

 `django_echarts.views.backend.EChartsBackendView` 

基于后端(template)的渲染视图类。

应用设置(App Settings)
-----------------------

下面的代码描述了项目的默认配置。

::

	{
		'echarts_version':'3.7.0',
		'lib_js_host':'bootcdn',
		'map_js_host':'echarts'，
		'local_host':None
	}


echarts_version
++++++++++++++++++++++

百度Echarts的版本字符串，如 `3.7.0`，大多数CDN的路径包含了字符串。

lib_js_host
++++++++++++++

**Echarts库文件(Echarts libary javascript file)** 的仓库名称或地址。以下均是有效的设置值：

- CDN名称: 包括了 `cdnjs` / `npmcdn` / ` bootcdn` / `pyecharts` / `echarts` 等5个。
- 代表实际url的格式化字符串，可使用的变量有以下几个，注意大小写区别：
    - STATIC_URL: `settings.STATIC_URL` 的值，如果不提供 `settings.STATIC_URL` ，将不会传递这个值。
    - echarts_version: 上面所述的版本字符串。

*lib_js_host* 能够支持的CDN及其实际url对应表如下：

+------------+--------------------------------------------------------------------+
| 名称       | url格式                                                            |
+============+====================================================================+
| cdnjs      | https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}   |
+------------+--------------------------------------------------------------------+
| npmcdn     | https://unpkg.com/echarts@{echarts_version}/dist                   |
+------------+--------------------------------------------------------------------+
| bootcdn    | https://cdn.bootcss.com/echarts/{echarts_version}                  |
+------------+--------------------------------------------------------------------+
| pyecharts  | https://chfw.github.io/jupyter-echarts/echarts                     |
+------------+--------------------------------------------------------------------+
| echarts    | http://echarts.baidu.com/dist                                      |
+------------+--------------------------------------------------------------------+

map_js_host
++++++++++++

**Echarts地图数据文件(Echarts map javascript file)** 的仓库名称或路径。可支持仓库名称如下表：

+------------+--------------------------------------------------------------------+
| 名称        |url格式                                                            |
+============+====================================================================+
| pyecharts  | https://chfw.github.io/jupyter-echarts/echarts                     |
+------------+--------------------------------------------------------------------+
| echarts    | http://echarts.baidu.com/asset/map/js                              |
+------------+--------------------------------------------------------------------+

>  注意: *echarts* CDN不支持HTTPS,当使用全站HTTPS引用非HTTPS外部资源在某些浏览器（如谷歌）会出现一些问题，建议先下载本地，再使用本地部署。

local_host
++++++++++++

本地仓库存储的路径，必须以 `settings.STATIC_URL` 的值开头。

项目配置访问(Project Settings Access)
--------------------------------------

DJANGO_ECHARTS_SETTINGS
++++++++++++++++++++++++

 `django_echarts.utils.DJANGO_ECHARTS_SETTINGS` 

 |  v0.1.3新增

在代码中，应当使用模块全局变量 `DJANGO_ECHARTS_SETTINGS` 访问项目的一些配置及其相关属性。该变量是类 `SettingsStore` 的一个实例。

DJANGO_ECHARTS_SETTING
+++++++++++++++++++++++++++

 | 已废弃

`DJANGO_ECHARTS_SETTINGS` 的别名，将在v0.2后移除。

SettingsStore
++++++++++++++++

 `django_echarts.utils.SettingsStore(**kwargs)` 

项目配置访问类

**host_store**

项目中的js仓库管理类，使用settings中的设置。

模板标签(Template Tags)
---------------------------

这些标签都定义在 *echarts* 模块，在使用之前需要先行导入。


echarts_options
++++++++++++++++++++

 `django_echarts.templatetags.echarts.echarts_options(echarts)` 

 | 已废弃，使用 `echarts_js_content` 代替。

渲染图表js代码。

echarts_container
++++++++++++++++++

 `django_echarts.templatetags.echarts.echarts_container(echarts_instance)` 

渲染图表容易(默认为 `<div></div>` )。

echarts_js_dependencies
+++++++++++++++++++++++++++++

 `django_echarts.templatetags.echarts.echarts_js_dependencies(*args)` 

渲染包含图表所需要的js文件的script一个或多个节点。

echarts_js_content
+++++++++++++++++++++++

 `django_echarts.templates.echarts.echarts_js_content(*echarts_list)` 

渲染图表初始js代码，支持多图表。包含首尾的  `<script></script>` 标签。

echarts_js_content_wrap
++++++++++++++++++++++++++

 `django_echarts.templates.echarts.echarts_js_content_wrap(*echarts_list)` 

渲染图表初始js代码，支持多图表。不包含首尾的  `<script></script>` 标签。

插件(Plugins)
----------------

*django-echarts* 提供了一些插件用于辅助功能。

Host
++++++++++

 `django_echarts.plugins.staticfiles.HostStore(name_or_host, context=None, host_lookup=None)` 

代表一个远程仓库的一个实体类，用于构建路径。

HostStore
+++++++++++

 `django_echarts.plugins.staticfiles.HostStore(context=None, echarts_lib_name_or_host=None, echarts_map_name_or_host=None, **kwargs)` 

一个仓库的集合，包含了若干个Host，和Host一样也能构建路径。

Jinja2Environment
++++++++++++++++++

 `django_echarts.plugins.jinja2.environment` 

jinja2模板引擎回调函数，返回 jinja2 模板引擎对象。

数据构建工具(Data Builder Tools)
----------------------------------

这些工具用于数据构建等方面。

Cast
++++++++

 `pyecharts.base.Base.cast(seq)` 

转化含有字段或数元组的序列到多个列表。

Pluck
++++++++

 `pluck.pluck(iterable, *keys, **kwargs)` 

选取一个或多个字段组成新的列表。

Django管理命令(Django Manage Commands)
---------------------------------------

这些命令可以从  *manage.py* 执行，支持其默认的参数， 详细可参考 [django-admin#default-options](https://docs.djangoproject.com/en/1.11/ref/django-admin/#default-options)。

::

	python manage.py COMMAND Foo1 Foo2


download_echarts_js
++++++++++++++++++++++


下载远程文件到本地

::
	usage: manage.py download_echarts_js [-h] [--version] [-v {0,1,2,3}]
										 [--settings SETTINGS]
										 [--pythonpath PYTHONPATH] [--traceback]
										 [--no-color] [--js_host JS_HOST]
										 js_name [js_name ...]


远程仓库的选择依据以下顺序

- `js_host` 参数
- `settings.DJANGO_ECHARTS['lib_js_host']` 或者 `settings.DJANGO_ECHARTS['map_js_host']` 