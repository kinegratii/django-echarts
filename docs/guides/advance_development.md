# 高级开发

本文提供了一些在扩展开发过程所需要的功能。这些功能的实现可能需要整合Django核心模块功能或者其他第三方库。

## 图表开发

### 自定义geojson

**1.  准备geojson文件**

根据实际业务需求制作geojson文件，并放置在项目 `BASE_DIR / 'static / 'geojson'` 目录之下。

**2. 引用geojson文件**

使用 `use_geojson` 引用地图文件。

```python
@site_obj.register_chart
def my_geojson_demo():
    map1 = Map()
    map1.add("", [('闽侯县', 23), ('湖里区', 45)], maptype="福建市县")
    map1.set_global_opts(title_opts=opts.TitleOpts(title="自定义geojson"))
    map1.height = '800px'
    use_geojson(map1, 'fujian.geojson', '福建市县')
    return map1
```

渲染后的前端代码如下（省略非关键代码）：

```javascript
$.getJSON("/geojson/fujian.geojson").done(function(mapdata){
    echarts.registerMap("福建市县", mapdata);
    var chart_3bf0d2a = echarts.init(
        document.getElementById('3bf0d2a'),
        'white',
        {renderer: 'canvas'}
    );
    var option_3bf0d2a = {
        "series": [
            {
                "type": "map",
                "mapType": "福建市县",
                "data": [
                    { "name": "闽侯县", "value": 23 },
                    { "name": "湖里区", "value": 45 }
                ],
            }
        ],
    };
    chart_3bf0d2a.setOption(option_3bf0d2a);
}).fail(function(jqXHR, textStatus, error){
    $("#3bf0d2a").html("Load geojson file fail!Status:" + textStatus);
});

```



## 组件

### 组件编写

django-echarts 内置的UI框架与下列项目是一样的，因此可以在项目中使用其提供模板标签以提高编码效率。

- Bootstrap3: [https://github.com/zostera/django-bootstrap3](https://github.com/zostera/django-bootstrap3)
- Bootstrap5: [https://github.com/zostera/django-bootstrap5](https://github.com/zostera/django-bootstrap5)
- Material: [https://github.com/viewflow/django-material](https://github.com/viewflow/django-material)



## 页面布局和逻辑

### 自定义内置页面功能

如果不想首页的默认布局和组件（大标题组件、热门图表等），也可以实现自己的视图和模板，只要路由保持不变即可。

使用步骤：

**1. 定义视图**

视图类必须继承 `DJESiteBackendView`，并重写 `dje_init_page_context` 方法，修改传给模板的变量字典 `context` 。

> Note: 方法 `dje_init_page_context` 如果有返回值，返回的应当是模板文件名称，而不是代表 context 的字典对象。

**2. 编写模板代码**

模板页面必须继承模板的 *base.html* 页面。在 *main_content* 部分编写模板代码。

```html
{% extends 'base.html' %}
{% load echarts %}

{% block main_content %}
<p>This is my nickname: {{ nickname }}</p>

{% endblock %}
```

**3. 关联路由**

使用 `DJESite.register_view()` 关联路由。

```python
class MyHomeView(DJESiteAboutView):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        pass


site_obj.register_view(view_name='dje_home', view_class=MyAboutView)
```

### 新的页面功能

django-echarts支持增加新页面功能。

**1. 定义视图和路由**

视图类必须继承 `DJESiteBackendView`，并重写 `dje_init_page_context` 方法，修改传给模板的变量字典 `context` 。

*site_views.py*

```python
class MyPageView(DJESiteBackendView):
    template_name = 'mypage.html'

    def dje_init_page_context(self, context, site: 'DJESite'):
        context['nickname'] = 'foo'


class MySite(DJESite):
    def dje_get_urls(self):
        return [
            path('mypage/', MyPageView.as_view(), name='dje_mypage')
        ]


site_obj = MySite()
```

**2. 定义模板**

模板页面必须继承模板的 *base.html* 页面。在 *main_content* 部分编写模板代码。方法同 *自定义内置页面功能* 一节。

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

