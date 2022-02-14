# 整合Django

本文提供了一些整合Django其他核心模块功能的方法。其中有一些是非官方的方法，可能涉及到其他第三方库。如果在整合过程中有什么疑惑，欢迎issues反馈或PR提交代码。

## 新的页面功能

django-echarts支持增加新页面功能。一个基本的功能实现由视图、模板、路由三部分组成。

**1. 定义视图类**

视图类必须继承 `DJESiteBaseView`，并重写 `dje_init_page_context` 方法，修改传给模板的变量字典 `context` 。

*site_views.py*

```python
class MyPageView(DJESiteBaseView):
    template_name = ttn('mypage.html')
    
    def dje_init_page_context(self, context, site: 'DJESite'):
        context['nickname'] = 'foo'

# 必须定义一个名为 urlpatterns 的模块变量，把本模块变为 URLconf module
urlpatterns =  site_obj.urls + [
    path('mypage/', MyPageView.as_view(), name='dje_mypage')
]
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

**3. 编写路由**

定义自己的路由规则。

```python
urlpatterns = [
    # ...
    url(r'', include(site_views)),
]
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
    path('site_demo/',decorator_include(login_required, site_obj.urls))
]
```

