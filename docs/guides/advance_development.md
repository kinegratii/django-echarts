# 高级开发

本文提供了一些在扩展开发过程所需要的功能。这些功能的实现可能需要整合Django核心模块功能或者其他第三方库。

> 在Django中，一个基本的功能实现由视图、模板、路由三部分组成。

## 修改内置页面的逻辑和模板

如果不想首页的默认布局和组件（大标题组件、热门图表等），也可以实现自己的视图和模板，只要路由保持不变即可。

使用步骤：

1. 视图类必须继承 `DJESiteBaseView`，并重写 `dje_init_page_context` 方法，修改传给模板的变量字典 `context` 。
2. 定义模板，模板必须继承 *base.html* ，放置在对应的模板路径下，如首页 *{TEMPLATE_DIR}{THEME}/home.html* 。

```python
class MyHomeView(DJESiteAboutView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        pass


site_obj.set_views(view_name='dje_home', view_class=MyAboutView)
```

## 新的页面功能

django-echarts支持增加新页面功能。

**1. 定义视图类**

视图类必须继承 `DJESiteBaseView`，并重写 `dje_init_page_context` 方法，修改传给模板的变量字典 `context` 。

*site_views.py*

```python
class MyPageView(DJESiteBaseView):
    template_name = ttn('mypage.html')

    def dje_init_page_context(self, context, site: 'DJESite'):
        context['nickname'] = 'foo'


class MySite(DJESite):
    def dje_get_urls(self):
        return [
            path('mypage/', MyPageView.as_view(), name='dje_mypage')
        ]


site_obj = MySite()
```

> Note: 方法 `dje_init_page_context` 如果有返回值，返回的应当是模板文件名称，而不是代表 context 的字典对象。

**2. 定义模板**

模板页面必须继承模板的 *base.html* 页面。在 *main_content* 部分编写模板代码。

```html
{% extends 'bootstrap3/base.html' %}
{% load echarts %}

{% block main_content %}
<p>This is my nickname: {{ nickname }}</p>

{% endblock %}
```

## 仅登录用户访问

django提供了 `login_required` 装饰器用于仅登录用户可访问的功能，但是该装饰器只能装饰视图函数。因此只能单独一个一个添加到对应视图函数之前。

[django-decorator-include](https://github.com/twidi/django-decorator-include) 是一个可以在装饰`include` 函数，使得对于同组的多个路由同时添加登录限制。

下面是一个例子：

```python
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from decorator_include import decorator_include

from site_views import site_obj

urlpatterns = [
    path('site_demo/', decorator_include(login_required, site_obj.urls))
]
```

## 组件编写

django-echarts 内置的UI框架与下列项目是一样的，因此可以在项目中使用其提供模板标签以提高编码效率。

- Bootstrap3: [https://github.com/zostera/django-bootstrap3](https://github.com/zostera/django-bootstrap3)
- Bootstrap5: [https://github.com/zostera/django-bootstrap5](https://github.com/zostera/django-bootstrap5)
- Material: [https://github.com/viewflow/django-material](https://github.com/viewflow/django-material)

## 修改布局和页面

根据 Django 的模板文件寻找逻辑即可实现。

第一，网站总体布局定义在 *{theme}/base.html* 文件之中，将该文件复制到你的项目模板文件目录之下。

```shell
python manage.py starttpl -t bootstrap5 -n base
```

第二，对新的文件进行修改，需要确保每个`block`都必须存在，否则其他页面无法继承。

> 参考资料：[Django Best Practices: Template Structure](https://learndjango.com/tutorials/template-structure)
