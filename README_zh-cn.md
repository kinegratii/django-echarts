# django-echarts

![django-echarts version](https://img.shields.io/pypi/v/django-echarts.svg) ![python27](https://img.shields.io/badge/Python-2.7+-blue.svg) ![python35](https://img.shields.io/badge/Python-3.5+-blue.svg) ![django18](https://img.shields.io/badge/Django-1.8+-blue.svg)

基于 [chenjiandongx/pyecharts](https://github.com/chenjiandongx/pyecharts) 的 [Echarts](http://echarts.baidu.com/index.html)和 [Django](https://www.djangoproject.com) 的整合库。

> 目前该项目还处于开发状态，不建议在生产环境中使用。


## 环境要求

- Python2.7+ / Python3.5+
- Django 1.8+
- echarts 3.1+

## 基本使用

views.py

```python
from django.views.generic.base import TemplateView
from pyecharts import Bar
from django_echarts import EchartsView

class IndexView(TemplateView):
    template_name = 'index.html'

class SimpleBarView(EchartsView):
    def get_echarts_option(self, **kwargs):
        bar = Bar("我的第一个图表", "这里是副标题")
        bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
        return bar._option
```

urls.py

```python
from django.conf.urls import url

from .views import IndexView, SimpleBarView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'options/simpleBar/', SimpleBarView.as_view())
]
```

html

```html
<div id="id_echarts_container" style="height: 500px;"></div>

<script type="text/javascript">
    $(document).ready(function () {
        var mChart = echarts.init(document.getElementById('id_echarts_container'));
        $.ajax({
            url: '/options/simpleBar/',
            type: "GET",
            dataType: "json"
        }).done(function (data) {
            mChart.setOption(data);
        });
    });
</script>
```

## API

(待定)

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