高级话题
=========

背景
-----

pyecharts_ 是一个优秀的 Echarts 的 Python 接口库，不仅实现了众多的图表类型，还支持在不同环境下（如纯Python、Jupyter Notebook以及web框架）运行。

.. _pyecharts: https://github.com/pyecharts/pyecharts

由于目标环境和使用场景的通用性，pyecharts 并不适合直接应用于 Django 项目。基于此， django-echarts 将遵循 Django 开发规范，试图简化开发工作，并增加了若干个 Django 项目特有的功能和特性。

django-echarts 是一个标准的 Django App ，符合其所有的使用规约，关于 Django 中 *项目(Project)* 和 *应用(Application)* 相关内容，可参考 https://docs.djangoproject.com/en/1.11/ref/applications/。

项目配置
-------------

定义
+++++

django-echarts 遵循统一配置的原则，所有的配置均定义在项目配置模块一个名为 `settings.DJANGO_ECHARTS` 变量中，该变量是一个字典类型。默认采用以下的配置：

::

	DJANGO_ECHARTS = {
		'echarts_version':'4.0.4',
		'renderer': 'canvas',
		'lib_js_host':'bootcdn',
		'map_js_host':'echarts'，
		'local_host':None
	}

该变量不建议作为配置访问的接口，关于如何访问配置信息请参考下面的内容。

访问
++++++

在开发中，使用全局变量 `django_echarts.conf.DJANGO_ECHARTS_SETTINGS` 访问项目配置值，支持以下字典形式访问：

- 键值访问 `DJANGO_ECHARTS_SETTINGS.get('echarts_version')` 。

`DJANGO_ECHARTS_SETTINGS` 还提供了若干个方法，用于获取当前项目的 js 依赖文件管理和其他功能配置。

以下是正确的使用方法：

::

    from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
    print(DJANGO_ECHARTS_SETTINGS.get('echarts_version'))

以下是不推荐的使用方法，不应当直接访问配置字典。

::

    from django.conf import settings
    print(settings.DJANGO_ECHARTS['echarts_version'])

SVG渲染配置
-------------

.. versionadded:: 0.3.1

ECharts 4.0 支持 SVG 渲染器。详细情况可以查看 文档_ 。

.. _文档: http://echarts.baidu.com/tutorial.html#%E4%BD%BF%E7%94%A8%20Canvas%20%E6%88%96%E8%80%85%20SVG%20%E6%B8%B2%E6%9F%93

django-echarts 默认使用 canvas 渲染器，可以通过以下方式更改为 svg 渲染。

::

	DJANGO_ECHARTS = {
	    'echarts_version':'4.0.4',
	    'renderer': 'svg'
	}

注意的是只有 echarts_version 大于 4 时，才可以使用 svg 渲染。django-echarts 并不会强制检查这一点，请使用者自行确认。

django-echarts 按照以下顺序选择渲染方式：

- 图表属性 `Chart.renderer`
- 项目配置的 `DJANGO_ECHARTS['renderer']` 的设置


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
- `django_echarts.datasets.charts.NamedCharts`

后端渲染
+++++++++

你可以按照 :doc:`tutorial` 所述的方法实现一个简单的后端渲染图表。

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

多图表渲染
----------

.. versionadded:: 0.3.4

自 v0.3.4 新增 `django_echarts.datasets.charts.NamedCharts` 用于多图表渲染，该类是对于原有的 `pyecharts.custom.page.Page` 进行改善，包括：

- 增加图表对象命名引用
- 移除了 `list` 的相关方法

基本使用
++++++++


在创建一个 `NamedCharts` 实例 `charts` ，后，使用 `add_chart` 添加一个图表对象，可以使用 `name` 为之起一个引用名称，如果没有指定引用名称，则使用 c0,c1 命名。

::


    class MultipleChartsView(EChartsBackendView):
        echarts_instance_name = 'charts'
        template_name = 'multiple_charts.html'

        def get_echarts_instance(self, *args, **kwargs):
            device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
            device_types, counters = fetch(device_data, 'device_type', 'count')
            pie = Pie("设备分类", page_title='设备分类', width='100%')
            pie.add("设备分类", device_types, counters, is_label_show=True)

            battery_lifes = models.Device.objects.values('name', 'battery_life')
            names, lifes = fetch(battery_lifes, 'name', 'battery_life')
            bar = Bar('设备电量', page_title='设备电量', width='100%')
            bar.add("设备电量", names, lifes)
            charts = NamedCharts().add_chart(pie, name='pie').add_chart(bar)
            return charts

元素访问
++++++++

.. versionchanged:: 0.3.5
   图表访问方式从 *属性访问* 改为 *字典访问* 。

对于 包含若干图表的 `NamedCharts` 实例，可以像字典一样访问该图表对象。

Python 代码的访问方式

::

    # 访问 pie 对象 page_title
    print(charts['pie'].page_title)

    # 访问 bar 对象 page_title
    print(charts['c1'].page_title) # 推荐
    print(charts[1].page_title) # 不再推荐

模板代码的访问方式：

::

    {{ charts.pie.page_title }}
    {{ charts.c1.page_title }}

注意

::

    无论是 Jinja2 模板还是 Django 模板，均不提倡使用 `charts.1` 形式访问列表中的某一个元素。

NamedCharts VS Page
+++++++++++++++++++

`NamedCharts` 内部使用 `collections.OrderedDict` 保存图表名称和实例，支持字典访问方式，同时扩展原有的 `Page` 的列表特性。

具体差别如下表：

.. image:: /_static/namedcharts-vs-page.png


模板标签
---------

django-echarts 实现了与 pyecharts 相似的模板标签,均定义在 `django_echarts.templatetags.echarts` 包，按文档有两种方式导入以这些标签能够使用。

- 在每个模板文件使用 `{% laod echarts %}` 导入。
- 添加标签目录到项目配置项 `TEMPLATES.OPTIONS.libraries`_ ，这样就无需在每个模板都使用 `load` 标签。

.. _TEMPLATES.OPTIONS.libraries: https://docs.djangoproject.com/en/1.11/topics/templates/#module-django.template.backends.django

这些标签接受一个或多个的图表实例作为参数。

.. image:: /_static/django-echarts-template-tags.png

和 pyecharts 所使用的 Jinja2 模板不同的是， Django 模板不支持 Python 调用，因此不支持 `{% echarts_js_content *page %}` 形式调用。

javascript文件管理
--------------------

仓库
+++++++

django-echarts 支持从多个地址引用 javascript 依赖文件，在引用某一个具体文件时，需指定仓库和文件名称两个值。

::

    django-echarts只支持外部链接方式，不支持内部嵌入方式。

如下面两个 js 文件链接例子中， `https://cdn.bootcss.com/echarts/3.7.0/` 和 `/static/js/` 称之为仓库地址。

::

    <script type="text/javascript" src="https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js"></script>
    <script type="text/javascript" src="/static/js/echarts.min.js"></script>

仓库为表示资源定位链接的字符串或字符格式串。

仓库分为本地和远程仓库两种，一般来说，以 `http://` 和 `https://` 开头的均视为远程仓库，其他则为本地仓库。


核心库文件和地图文件
+++++++++++++++++++++++++++++

由于不同仓库提供的 js 不同，django-echarts 将相关其大致分为两类：

- 核心库文件(lib)
- 地图文件(map)

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
- 常量 `'local_host'`：表示使用 `local_host` 相同的配置。

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
| pyecharts  | https://pyecharts.github.io/jupyter-echarts/echarts                |
+------------+--------------------------------------------------------------------+
| echarts    | http://echarts.baidu.com/dist                                      |
+------------+--------------------------------------------------------------------+

表：内置 CDN 列表

**版本号**

这些 CDN 地址通常依赖于 ECharts 版本，可以在 `DJANGO_ECHARTS['echarts_version']` 中设置具体的版本号，如 `3.7.0` 。

关于如何选择合适的 ECharts 的版本号，请参考 pyecharts 文档。

**网络协议**

除了 echarts 官方网址外，均采用 HTTPS 协议地址。 echarts 和 pyecharts 不是正式CDN，仅供演示，不建议运用于实际环境，可下载本地部署。

CLI工具
--------

django-echarts 提供了一个包含若干个命令的 CLI 工具，这些命令都是标准的 Django 管理命令，均定义在 `django_echarts.management.commands` 包下。

你可以使用以下命令查看帮助信息。

::

    python manage.py <command> -h

文件下载
++++++++

.. versionadded:: 0.2.2
    新增 `download_lib_js` 和 `download_map_js` 命令。

django-echarts 提供了一些下载命令，可以从远程地址下载文件到项目的静态目录中。这些命令包括：

- download_echarts_js 通用下载
- download_lib_js 下载 Echarts 核心库
- download_map_js 下载 地图文件

使用用法可用 `-h` 查看：

.. code-block:: none

    usage: manage.py download_echarts_js [-h] [--version] [-v {0,1,2,3}]
                                         [--settings SETTINGS]
                                         [--pythonpath PYTHONPATH] [--traceback]
                                         [--no-color] [--js_host JS_HOST] [--fake]
                                         js_name [js_name ...]

    Download one or some javascript files from remote CDN to project staticfile
    dirs.

    positional arguments:
      js_name

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Raise on CommandError exceptions
      --no-color            Don't colorize the command output.
      --js_host JS_HOST     The host where the file will be downloaded from.
      --fake                Print the remote url and local path.


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

    python manage.py download_echarts_js echarts.min china fujian anhui

`download_echarts_js` 支持同时下载核心库和地图文件，根据 `django_echarts.plugins.hosts.JsUtils.is_lib_js` 区分。如果你出现文件归类错误，可以使用更为明确的命令。

如上述了例子也可以分为下面两个命令

::

    python manage.py download_lib_js echarts.min
    python manage.py download_map_js fujian anhui


download_echarts_js内部采用 Python 标准库的 `urllib.request.urlopen`_ 函数实现文件下载。如果在执行过程中出现错误，请依据该函数文档进行排查。

.. _urllib.request.urlopen: https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen
