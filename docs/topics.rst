高级话题
=========

背景
-----

pyecharts_ 是一个优秀的 Echarts 的 Python 接口库，不仅实现了众多的图表类型，还支持在不同环境下（如纯Python、Jupyter Notebook以及web框架）运行。

.. _pyecharts: https://github.com/chenjiandongx/pyecharts

由于目标环境和使用场景的通用性，pyecharts 并不适合直接应用于 Django 项目。基于此， django_echarts 将遵循 Django 开发规范，试图简化开发工作，并增加了若干个 Django 项目特有的功能和特性。

django_echarts 是一个标准的 Django App ，符合其所有的使用规约，关于 Django 中 *项目(Project)* 和 *应用(Application)* 相关内容，可参考 https://docs.djangoproject.com/en/1.11/ref/applications/。

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

该变量不建议作为配置访问的接口，关于如何访问配置信息请参考下面的内容。

django_echarts 目前不接受对象级别的配置，因此 `pyecharts.base.Base.jshost` 和 `pyecharts.custom.page.Page.jshost` 两个属性无效，应当在 `settings.DJANGO_ECHARTS` 中统一配置。

访问
++++++

在开发中，使用全局变量 `django_echarts.utils.DJANGO_ECHARTS_SETTINGS` 访问项目配置值，支持以下两种形式访问：

- 键值访问：如 `DJANGO_ECHARTS_SETTINGS['echarts_version']` 。
- 属性访问，如 `DJANGO_ECHARTS_SETTINGS.echarts_version` 。

`DJANGO_ECHARTS_SETTINGS` 还提供了若干个方法，用于 js 依赖文件管理和其他功能。

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

- 后端：通过模板标签/标签渲染页面
- 前端：先渲染页面，数据通过 Ajax 异步请求返回

两者渲染方式具有共同的接口，均继承自 `django_echarts.views.base.EChartsMixin` 。

::

    class EChartsMixin(object):
        def get_echarts_instance(self, *args, **kwargs):
            pass

函数 `get_echarts_instance` 需要返回一个图表实例对象，包括：

- `pyecharts.base.Base`
- `pyecharts.custom.page.Page`

后端渲染
+++++++++

你可以按照 :ref:`tutorial-start` 文档所述的方法实现一个简单的后端渲染图表。

`EChartsBackendView` 是后端渲染方式主要使用的视图类，该类继承自 `django.views.generic.base.TemplateView`，因此返回给浏览器的是一个 TemplateResponse 对象。

前端渲染
+++++++++

渲染需要继承 `EChartsFrontendView` 类，和后端渲染方式不同的是，该视图类返回是 chart.options 的 json 字符串，而前端需要使用 ajax 等方式接收数据，并且需要使用 `setOption` 函数设置信息。

.. code-block:: guess

    <script src="https://cdn.bootcss.com/echarts/3.6.2/echarts.min.js"></script>
    <script src="http://echarts.baidu.com/asset/map/js/china.js"></script>
    <script type="text/javascript">
        var mChart;
        function loadEcharts() {
            var url = '/options/simpleBar/;
            if (mChart != null) {
                mChart.clear();
            }
            mChart = echarts.init(document.getElementById('id_echarts_container'));
            mChart.showLoading();
            $.ajax({
                url: url,
                type: "GET",
                data: null,
                dataType: "json"
            }).done(function (data) {
                mChart.hideLoading();
                mChart.setOption(data);
            });
        }
        $(document).ready(function () {
            loadEcharts('simpleBar');
        });
    </script>

模板标签
---------

django_echarts 实现了与 pyecharts 相似的模板标签,均定义在 `django_echarts.templatetags.echarts` 包，按文档有两种方式导入以这些标签能够使用。

- 在每个模板文件使用 `{% laod echarts %}` 导入。
- 添加标签目录到项目配置项 `TEMPLATES.OPTIONS.libraries`_ ，这样就无需在每个模板都是用 `load` 标签。

.. _TEMPLATES.OPTIONS.libraries: https://docs.djangoproject.com/en/1.11/topics/templates/#module-django.template.backends.django

这些标签接受一个或多个的图表实例作为参数。

.. image:: /_static/django-echarts-template-tags.png

和 pyecharts 相比，这些标签函数有以下不同之处：

- 不支持 `{% echarts_js_content *page %}` 形式调用。

javascript文件管理
--------------------

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

由于不同仓库提供的 js 不同，django_echarts 将相关其大致分为两类：

- 核心库文件
- 地图文件

以下文件常用 CDN 都有携带的文件，均被视为是核心库文件，

::

    ECHARTS_LIB_NAMES = [
        'echarts.common', 'echarts.common.min',
        'echarts', 'echarts.min',
        'echarts.simple', 'echarts.simple.min',
        'extension/bmap', 'extension/bmap.min',
        'extension/dataTool', 'extension/dataTool.min'
    ]

涉及 js 仓库设置的选项有三个：

- lib_js_host: 指定 Echarts 核心库文件的仓库
- map_js_host: 指定地图文件的仓库
- local_host: 本地仓库的具体路径

一般来说，只需设置 `lib_js_host` 和 `map_js_host` 两个值即可，它们均支持以下几种形式的值：

- 地址字符串：如 `http://115.00.00.00:8080/echarts/` 。
- 地址格式化字符串：类似于 Python 格式化，使用 `{}` 嵌入变量，如 `'{STATIC_URL}/js/echarts'` 、 `'https://demo.com/{echarts_version}'` 等。
- CDN名称：参见下一节 “公共CDN”。

举个例子，下面是某一个 Django 项目的静态文件目录结构。

::

    - example
        - example
            - __init__.py
            - settings.py
            - urls.py
            - wsgi.py
        - static
            - echarts/
                - echarts.min.js
            - map/
                - beijing.js
                - china.js
                - fujian.js
        - demo
            - __init__.py
            - urls.py
            - views.py

如果想达到上述的目录布局，相应的 `settings.py` 相关设置可设置为：

::

    STATIC_URL = '/static/'

    DJANGO_ECHARTS = {
        'lib_js_host':'/static/echarts',
        'map_js_host': '/static/map'
    }

需要注意的是：

- 路径末尾 `/` 添加或不添加均可。
- 无论核心库和地图文件是否在同一个目录，都要同时设置。

公共CDN
++++++++

django_echarts 内置几个常用的 CDN ，你可以只写名称而不是具体的 url 地址， django_echarts 将自动使用对应的地址。


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

表：内置 CDN 列表

**版本号**

这些 CDN 地址通常依赖于 ECharts 版本，可以在 `DJANGO_ECHARTS['echarts_version']` 中设置具体的版本号，如 `3.7.0` 。

关于如何选择合适的 ECharts 的版本号，请参考 pyecharts 文档。

**网络协议**

除了 echarts 官方网址外，均采用 HTTPS 协议地址。 echarts 和 pyecharts 不是正式CDN，仅供演示，不建议运用于实际环境，可下载本地部署。

数据构建
---------

`pyecharts.base.Base.add` 函数通常要求数据是两个长度相等的列表。

如果原始数据是其他形式的字典或元组列表，pyecharts 和 django_echarts 提供了若干个可以数据构建和转化的函数，以适配图表的相关方法。

例如内置的 `zip` 函数，可将列表按元素键名分解成多个列表。


::

        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        # t_data = [(21, '2017-12-01'), (19, '2017-12-02'), (20, '2017-12-03')]
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)

又比如，django_echarts 内置了 `pluck` 库，提供了其他形式的数据转化，下面是一个比较典型的例子。

使用方法如下：

*pluck_demo.py*

.. literalinclude:: /codes/pluck_demo.py

更多可查看其主页 https://github.com/nvie/pluck 。

自 v0.2.1 起，新增 `django_echarts.plugins.fetch.fetch` 是对原有 pluck + zip 函数的进一步封装。

如

::

    from pyecharts import Bar
    from django_echarts.plugins.fetch import fetch

    objects = [
        {'id': 282, 'name': 'Alice', 'age': 30},
        {'id': 217, 'name': 'Bob', 'age': 56},
        {'id': 328, 'name': 'Charlie', 'age': 56},
    ]

    names, ages = fetch(objects, 'name', 'age')

    bar = Bar()
    bar.add('The Age of Members', names, ages)

特别的是，对于复杂的关系图，可以使用 networkx_ 库构建节点和连线，并传递给 `add` 函数。

.. _networkx: https://github.com/networkx/networkx

*graph_demo.py*

.. literalinclude:: /codes/graph_demo.py

渲染后的关系图如下：

.. image:: /_static/networkx-graph-demo.png


更多信息可查看 API 文件。

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

.. code-block:: none

    Download file from https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js
    Save file to F:\django-echarts\example\static\echarts\echarts.min.js

注意在使用该命令之前需要保证其父目录必须存在，否则将保存失败。

download_echarts_js 还支持同时下载多个文件，如：

::

    python manage.py download_echarts_js echarts.min china fujian


download_echarts_js内部采用内置的 `urlopen` 函数实现文件下载。如果在执行过程中出现错误，请依据该函数文档进行排查。