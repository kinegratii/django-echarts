# 网站构建

正如 *快速开始*  一节所提到的，django-echarts 提供了一个简单便捷的脚手架工具包，她负责处理底层的视图逻辑、URL路由、模板、前端界面及其之间的连结，你只需编写构建图表的pyecharts代码。

## 网站架构

网站可视化提供了一种用户友好的前台界面（和django-admin后台管理界面相对应）。主要由以下几个页面组成：

| 功能页面 | 描述                                                     | 默认实现视图类    |      |
| -------- | -------------------------------------------------------- | ----------------- | ---- |
| 基础页面 | 负责网站的整体布局、风格，组件包括头部导航栏、底部版权栏 | -                 |      |
| 首页     | 大标题、热门/推荐图表组件                                | DJESiteHomeView   |      |
| 列表页面 | 显示所有图表的基本信息，支持分页                         | DJESiteListView   |      |
| 详情页面 | 显示由echarts渲染的可交互图表                            | DJESiteDetailView |      |
| 关于页面 | 显示基本信息                                             | DJESiteAboutView  |      |



## 站点（DJESite）

`DJESite` 是所有界面和逻辑的入口点，首先必须创建你自己的 site 对象。

```python
from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
from django_echarts.starter.sites import DJESite, DJESiteDetailView

site_obj = DJESite(
    site_title='图表可视化',
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts')
)
```

对象创建时，可以设置以下参数：

- site_title: 网站标题
- theme:界面主题，目前仅支持 bootstrap3及其部分调色主题 。
- copyright_:底部版本信息。

> 如果参数或变量和内置函数的名称相同，将在最后加下划线以示区分。

### 导航栏(Nav)

顶部导航栏是一个有二级菜单的导航功能，下列的菜单项默认已添加：

- 首页 `Menu(text='首页', slug='home', url=reverse_lazy('dje_home'))`
- 列表`Menu(text='列表', slug='list', url=reverse_lazy('dje_list'))`
- DetailView中已经包含的图表，每一个图表是一个二级菜单项

也可以通过 `DJESite` 提供的方法添加自定义链接。

```python
from django.urls import reverse_lazy
from django_echarts.starter.html_widgets import LinkItem

# 在右侧添加项目仓库链接，以新标签页方式打开
item = LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True)
site_obj.add_link(item)

item2 = LinkItem(text='关于', url=reverse_lazy('detail'))
site_obj.add_menu_item(item2)
```

类 `LinkItem` 表示一个超链接，url可以设置链接文本，也可以使用视图名称反向解析。

> 注意：使用视图反向解析时必须使用 `reverse_lazy`，而不是 `reverse`，否则出现无法解析的异常。因为此时 site_obj 还未挂载到项目全局的 url 路由规则之中。



### 底部版权栏(Copyright)

`Copyright` 类用于初始化页面底部的版权文字。可以传入的参数有：

- start_year：开始的年份
- powered_by: 版权主题名称

例子 `Copyright(start_year=2017, powered_by='Django-Echarts')` 的将渲染为下列文字：

```
©2017-2022, Powered By Django-Echarts
```



### 注册视图

当需要在某个页面实现自己的逻辑时，可以继承相应的实现视图类，重写相关属性和方法，然后调用对应的方法注册到 site_obj 对象之中。

```python
DJESite.register_home_view(view_class: Type[DJESiteHomeView])
DJESite.register_list_view(view_class: Type[DJESiteListView])
DJESite.register_detail_view(view_class: Type[DJESiteDetailView])
DJESite.register_about_view(view_class: Type[DJESiteAboutView])
```

一般来说，诸如Home/List/About等仅显示静态数据的页面，`DJESite` 提供了更为简洁的方式实现，而不必显式调用这些注册函数。比如 `DJESite.paginate_by` 属性等。

### 自定义模板文件

所有的视图类均继承 `django.views.generic.base.TemplateView` ，因此可以通过重写 `template_name` 重新指定相应的模板文件。

另外，一些视图（如DJESiteListView和DJESiteDetailView）会使用到不同的模板文件，这些变量名称通常以 `*_template_name` 的方式存在。

```python
class MyChartDetailView(DJESiteDetailView):
    template_name = 'my_detail.html'
    empty_template_name = 'my_empty.html'
```

指定的模板文件名称可以是具体字符串，也可以是待赋值的字符串，比如 `'{theme}/home.html'`。Site将传入下列变量：

- theme: 主题名称

### 模板API

各个子页面均继承自 `DJESiteBaseView` ，页面渲染时向模板传入下列数据。

| 特性     | 模板              | 变量名称   | 类型                        | 说明         |
| -------- | ----------------- | ---------- | --------------------------- | ------------ |
| 基础逻辑 | {theme}/base.html | site_title | `str`                       | 网站标题     |
|          |                   | theme      | `str`                       | 主题名称     |
|          |                   | nav        | `starter.widgets.Nav`       | 顶部导航栏   |
|          |                   | copyright  | `starter.widgets.Copyright` | 底部版权信息 |



## 首页（Home）

首页主要包括大标题组件和热门/推荐组件。

- 视图类：DJESiteHomeView

### 模板API

| 特性 | 模板              | 变量名称       | 类型                        | 说明               |
| ---- | ----------------- | -------------- | --------------------------- | ------------------ |
| 首页 | {theme}/home.html | jumbotron      | `starter.widgets.Jumbotron` | 大标题             |
|      |                   | top_chart_list | `List[DJEChartInfo]`        | 热门推荐的图表信息 |



## 列表页面（List）

列表页面按照列表方式显示了所有图表的基本信息，默认实现类 `DJESiteListView` 。

### 设置分页

有两种方式设置，第一种在site创建时传入 `paginate_by` 参数，指定每页需要显示的数目，默认不启用分页特性。

```python
site_obj = DJESite(
    site_title='图表可视化',
    paginate_by=10
)
```

第二种，如果需要替换默认的模板文件，继承 `DJESiteListView`，重新指定 paginator_template_name 即可。

```python
class MyListListView(DJESiteListView):
    paginator_template_name = 'my_paginator_list.html'
    paginate_by = 15

site_obj.register_list_view(MyListListView)
```

需要注意的是，MyListListView中paginate_by值将覆盖site初始化传入的值，比如上述两个片段整合时paginate_by即为15。

### 模板API

根据是否具有分页特性，使用不同的模板文件，并传入不同模板变量。

| 特性   | 模板                             | 变量名称   | 类型                         | 说明                                     |
| ------ | -------------------------------- | ---------- | ---------------------------- | ---------------------------------------- |
| 无分页 | {theme}/list.html                | chart_list | `List[DJEChartInfo]`         | 图表的基本信息，包括标题、标识、介绍文本 |
| 有分页 | {theme}/list_with_paginator.html | page_obj   | `django.core.paginator.Page` | django构建的分页对象。                   |

备注：

- 其中page_obj.obj_list 是具体的条目数据，类型与chart_list相关，其他属性可以参见 [《Django Paginator 》](https://docs.djangoproject.com/en/4.0/topics/pagination/)。



## 详情页面（Detail）

### 构建pyecharts图表-FBV

`site_obj.register_chart` 装饰器用于注册返回图表的函数。

```python
@site_obj.register_chart
def mychart():
    bar = Bar()
    # ...
    return bar
```

默认未携带任何参数情况下，函数名将作为图表标识符。

当然也可以携带一些参数，这些参数通常和 `DJEChartInfo` 类参数意义相同。

```python
@site_obj.register_chart(description='词云示例', menu_text='示例一')
def mychart():
    bar = Bar()
    # ...
    return bar
```



### 构建pyecharts图表-CBV

类方式（Clased-base view）通常是将具有紧密意义的图表组成一组，在代码上以类方式体现。

```python
class MyDemoDetailView(DJESiteDetailView):
    charts_config = [('c1', '柱形图'), ('c2', '饼图')]

    def dje_chart_c1(self, *args, **kwargs):
        bar = Bar()
        # ...
        return bar

    def dje_chart_c2(self, *args, **kwargs):
        pie = Pie()
        # ...
        return pie


site_obj.register_detail_view(MyDemoDetailView, menu_text='示例一')
```

函数名称必须符合 `"dje_chart_<chart_name>"` 的格式要求。

### 模板API

根据是否存在对应的图表，显示不同的模板。

| 特性   | 模板                | 变量名称  | 类型                   | 说明                                     |
| ------ | ------------------- | --------- | ---------------------- | ---------------------------------------- |
| 有图表 | {theme}/detail.html | menu      | `List[DJEChartInfo]`   | 图表的基本信息，包括标题、标识、介绍文本 |
|        |                     | chart_obj | `pycharts.charts.Base` | 图表对象。                               |
| 无图表 | {theme}/empty.html  | -         | -                      | -                                        |

## 关于页面（About）



### 模板API



| 特性     | 模板               | 变量名称 | 类型 | 说明 |
| -------- | ------------------ | -------- | ---- | ---- |
| 关于页面 | {theme}/about.html | -        | -    | -    |
