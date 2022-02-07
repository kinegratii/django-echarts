# 整合Django

本文提供了一些整合Django其他核心模块功能的方法。其中有一些是非官方的方法，可能涉及到其他第三方库。如果在整合过程中有什么疑惑，欢迎issues反馈或PR提交代码。

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

