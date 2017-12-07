高级文档
=========

django_echarts是什么
--------------------

pyecharts 是一个优秀的 Echarts 的 Python 接口库，不仅实现了众多的图表类型，还支持在不同环境下（如纯Python、Jupyter Notebook以及web框架）运行。

由于目标环境和使用场景的通用性，pyecharts 并不适合直接适用于 Django 项目。基于此， django_echarts 试图简化 pyecharts 的使用方法，并增加了若干个 Django 项目特有的功能和特性。


项目配置
-------------

定义
+++++

django-echarts 遵循统一配置的原则，所有的配置均定义在项目配置模块一个名为 `settings.DJANGO_ECHARTS` 变量中，该变量是一个字典类型。如果没有任何配置采用以下的默认值：

::

	DJANGO_ECHARTS = {
		'echarts_version':'3.7.0',
		'lib_js_host':'bootcdn',
		'map_js_host':'echarts'，
		'local_host':None
	}

该变量不建议作为配置访问的接口，关于如何访问配置信息请参考下一节的内容。

django_echarts 目前不接受对象级别的配置，因此 `pyecharts.base.Base.jshost` 和 `pyecharts.custom.page.Page.jshost` 两个属性无效，应当在 `settings.DJANGO_ECHARTS` 中统一配置。

访问
++++++

在开发中，使用全局变量 `django_echarts.utils.DJANGO_ECHARTS_SETTINGS` 访问项目配置值，支持以下两种形式访问：

- 键值访问：如 `DJANGO_ECHARTS_SETTINGS['echarts_version']` 。
- 属性访问，如 `DJANGO_ECHARTS_SETTINGS.echarts_version` 。

`DJANGO_ECHARTS_SETTINGS` 还提供了若干个方法，用于 js 依赖文件管理的整合以及整合其他功能。

以下是正确的使用方法：

::

    from django_echarts.utils import DJANGO_ECHARTS_SETTINGS
    print(DJANGO_ECHARTS_SETTINGS.echarts_version)

以下是不推荐的使用方法，不应当直接访问配置字典。

::

    from django.conf import settings
    print(settings.DJANGO_ECHARTS['echarts_version'])


视图渲染
---------

django_echarts 提供两种方式的渲染视图，即：

- 后端：数据和图表一起返回
- 前端：先渲染页面，数据通过 Ajax 异步请求返回

两者渲染方式具有共同的接口 `get_echarts_instance` 。

后端渲染
+++++++++

后端渲染方式需继承 `EChartsBackendView` 类。

前端渲染
+++++++++

和后端渲染方式不同的是，渲染一个图表通常需要两个请求

js文件管理
----------

仓库
+++++++

django_echarts 支持从多个地址引用 javascript 依赖文件，在引用某一个具体文件时，需指定仓库和文件名称两个值。

::

    django_echarts只支持外部链接方式，不支持内部嵌入方式。

如下面两个 js 文件链接例子中， `https://cdn.bootcss.com/echarts/3.7.0/` 和 `/static/js/` 称之为仓库地址。

::

    <script type="text/javascript" src="https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js"></script>
    <script type="text/javascript" src="/static/js/echarts.min.js"></script>

仓库为表示资源定位链接的字符串或字符格式串。

仓库分为本地和远程仓库两种，一般来说，以 `http://` 和 `https://` 开头的均视为远程仓库，其他则为本地仓库。


核心库文件和地图文件
+++++++++++++++++++++++++++++

django_echarts 将相关 js 文件分为两类：

- 核心库文件
- 地图文件


数据构建
---------

django_echarts 还提供了若干个可以数据构建和转化的函数，以适配图表的相关方法。更多信息可查看 API 文件。

Jinja2模板引擎
--------------

自 Django v1.8 起，Django 支持多模板引擎，内置了 Jinja2 模板引擎。 如果你的项目是采用 jinja2 模板引擎来渲染页面，通过简单的代码，就可以在你的项目直接使用 pyecharts 提供的 jinja2 模板函数。

只需将 `OPTIONS.environment` 指向 `django_echarts.plugins.jinja2.environment` 回调函数。



::

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'environment': 'django_echarts.plugins.jinja2.environment'
            },
        },
    ]

其余选项设置可参考 `Django 官方文档`_ 。

.. _Django 官方文档: https://docs.djangoproject.com/en/1.11/topics/templates/#django.template.backends.jinja2.Jinja2

CLI工具
--------

django_echarts 提供了一个包含若干个命令的 CLI 工具，这些命令都是标准的 Django 管理命令，均定义在 `django_echarts.management.commands` 包下。

你可以使用以下命令查看帮助信息。

::

    python manage.py <command> -h

文件下载
++++++++

download_echarts_js 命令将从远程地址下载文件到项目的静态目录中。

::

    usage: manage.py download_echarts_js [-h] [--version] [-v {0,1,2,3}]
                                         [--settings SETTINGS]
                                         [--pythonpath PYTHONPATH] [--traceback]
                                         [--no-color] [--js_host JS_HOST]
                                         js_name [js_name ...]

在使用之前需进行一些配置，如下面的例子：

::

    STATIC_URL = '/static/'

    DJANGO_ECHARTS = {
    	'echarts_version':'3.7.0',
    	'lib_js_host':'bootcdn',
    	'map_js_host':'echarts'
        'local_host': '{STATIC_URL}echarts'
    }

其中 `local_host` 是必须配置为本地的文件下载目标目录。

使用 `python manage.py download_echarts_js echarts.min` 从 boot CDN 下载 echarts.min.js 文件到项目的静态文件存储目录之下，相关输出如下：

::

    Download file from https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js
    Save file to F:\django-echarts\example\static\echarts\echarts.min.js

注意在使用该命令之前需要保存其父目录必须存在，否则将保存失败。

download_echarts_js 还支持同时下载多个文件，如：

::

    python manage.py download_echarts_js echarts.min china fujian


download_echarts_js内部采用内置的 `urlopen` 函数实现文件下载。