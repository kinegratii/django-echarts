# 高级开发

本文提供了一些在扩展开发过程所需要的功能。这些功能的实现可能需要整合Django核心模块功能或者其他第三方库。

## 图表开发



## 组件

### 组件编写

django-echarts 内置的UI框架与下列项目是一样的，因此可以在项目中使用其提供模板标签以提高编码效率。

- Bootstrap3: [https://github.com/zostera/django-bootstrap3](https://github.com/zostera/django-bootstrap3)
- Bootstrap5: [https://github.com/zostera/django-bootstrap5](https://github.com/zostera/django-bootstrap5)
- Material: [https://github.com/viewflow/django-material](https://github.com/viewflow/django-material)



## 视图逻辑

### 仅登录用户访问

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

### 用户名显示

`DwString` 提供了一种利用模板字符串显示动态字符串的功能。

例子：在右侧菜单栏显示用户信息，如果登录则显示用户名（`request.user.username`），未登录显示“匿名用户” 文字。

```python
site_obj.add_right_link(
    LinkItem(text=DwString.login_name(un_login_text='匿名用户'))
)
```

