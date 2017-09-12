# Django-Echarts Document

## Quicksart

django-echarts is a django app for the intergration of django and pyecharts.

1 Create your django project at any folder.

2 Create your view based on CBV or FBV.

3 Write your template.

## Basic Usage

### Use Template Render

1 Create your view base CBV or FBV.

```python
from django.views.generic.base import TemplateView
from pyecharts import Bar

class SimpleBarTemplateView(TemplateView):
    tempalate = 'simple_bar.html'
    
    def get_context_data(self, **kwargs):
        context = super(SimpleBarTemplateView, self).get_context_data(**kwargs)
        bar = Bar("我的第一个图表", "这里是副标题")
        bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
        context['bar'] = bar
        return context
```

2 Create template file.

```html
 {% load echarts %}
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Django Echarts Demo</title>
</head>
  <body>
    <div id="{{ bar._chart_id }}" style="height: 500px;"></div>
    {% echarts_js_dependencies bar %}
    {% echarts_js_content bar %}
  </body>
</html>
```

### Use Ajax Render

1 Create your view class.

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

2 Add views to the urls module.

```python
from django.conf.urls import url

from .views import IndexView, SimpleBarView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'options/simpleBar/', SimpleBarView.as_view())
]
```

3 Create template html

```html
{% load echarts %}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Django Echarts Demo</title>
</head>
<body>
<div id="id_echarts_container" style="height: 500px;"></div>
{% echarts_js_dependencies 'echarts.min' %}
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
</body>
</html>
```
### FAQ

1 If load echarts every template page.