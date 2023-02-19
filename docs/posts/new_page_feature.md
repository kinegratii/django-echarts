# 新的页面功能

## 1 概述

`django_echarts.starter` 支持新增新的页面功能，一个基本的页面功能由视图、路由和模板组成。

## 2 使用步骤

### 创建新的视图

视图类必须继承 `DJESiteBackendView`，并重写 `get_context_data` 方法，添加自己的数据到 `context`，并返回该字典 。

```python
class MyPageView(DJESiteBackendView):
    template_name = 'mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nickname'] = 'foo'
        return context
```

### 编写模板代码

模板页面必须继承模板的 *base.html* 页面。在 *main_content* 部分编写模板代码。

```html
{% extends 'base.html' %}
{% load echarts %}

{% block main_content %}
<p>This is my nickname: {{ nickname }}</p>

{% endblock %}
```

### 关联路由

将新路由和 `site_obj.urls` 合并。

```python
site_obj = MySite()

site_obj.extend_urlpatterns([
    path('mypage/', MyPageView.as_view(), name='view_my_page')
])
```

### 添加到导航栏

```python
site_obj.add_left_link(
    LinkItem(title='我的页面', url=reverse_lazy('view_my_page')),
    menu_title='菜单一'
) # 作为“菜单一”的二级菜单
```

