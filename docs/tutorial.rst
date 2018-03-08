.. _tutorial-start:

入门教程
=========

安装
------

自 v0.3 开始，django-echarts 只支持 Python3.5以上 的开发环境。

::

    pip install django-echarts

如果使用的是 Python2 的环境，可以使用 0.2.X 系列的最新版本。

::

    pip install django-echarts==0.2.3

如若使用最新的开发版本，可使用源码构建

.. code-block:: none

	git clone https://github.com/kinegratii/django-echarts.git
	cd django-echarts
	python setup.py install


快速使用
---------

1 添加 django_echarts包到项目配置模块的 `INSTALL_APPS` 列表。

::

	INSTALL_APPS = (
		# Your apps
		'django_echarts',
		# Your apps
	)


2 根据实际场景需要设置一些配置参数，这些参数必须定义在项目模块中一个名为 `DJANGO_ECHARTS` 的字典里。

::

	DJANGO_ECHARTS = {
	    'echarts_version': '4.0.4',
	    'lib_js_host':'cdnjs'
	}

由于不同 ECharts 版本会有一些功能和形式上的区别，建议自行指定某一个版本。

更多可选值请参 API 文档。

3 编写视图类，模板页面和路由。

::

	def create_simple_bar():
		bar = Bar("我的第一个图表", "这里是副标题")
		bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
		return bar

	 class BackendEChartsTemplate(EChartsBackendView):
		template_name = 'backend_charts.html'

		def get_echarts_instance(self, *args, **kwargs):
			return create_simple_bar()


4 编写模板文件，可以使用相关标签（定义在 `echarts` 标签库里）渲染JS内容。

.. code-block:: html

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


5 在部署到正式环境时，如果需要使用公共CDN托管常用JS文件，可修改项目配置，使得 `lib_js_host` 或者 `map_js_host` 指向公共CDN。

示例项目
---------

示例项目请参考 example 文件夹。

.. code-block:: shell

    cd example
    python manage.py runserver 127.0.0.1:8000


访问本地地址： http://127.0.0.1:8000 ，示例运行结果

.. image:: /_static/django-echarts-demo.gif