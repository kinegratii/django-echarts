# 布局和架构

正如 *快速开始*  一节所提到的，django-echarts 提供了一个简单便捷的脚手架工具包，她负责处理底层的视图逻辑、URL路由、模板、前端界面及其之间的连结，你只需编写构建图表的pyecharts代码。

## 网站架构

网站可视化提供了一种用户友好的前台界面（和django-admin后台管理界面相对应）。主要由以下几个页面组成：

| 功能页面 | 功能特性                                                 | 默认实现视图类    |      |
| -------- | -------------------------------------------------------- | ----------------- | ---- |
| 基础页面 | 负责网站的整体布局、风格，组件包括头部导航栏、底部版权栏 | -                 |      |
| 首页     | 大标题、热门/推荐图表组件                                | DJESiteHomeView   |      |
| 列表页面 | 显示所有图表的基本信息，支持分页                         | DJESiteListView   |      |
| 详情页面 | 显示由echarts渲染的可交互图表                            | DJESiteDetailView |      |
| 关于页面 | 显示基本信息                                             | DJESiteAboutView  |      |



## 初始化站点

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

| 参数            | 类型或可选值   | 描述                                                 |
| --------------- | -------------- | ---------------------------------------------------- |
| site_title      | str            | 网站标题                                             |
| theme           | str            | 内置 bootstrap3/bootstrap3.cerulean/material三个主题 |
| copyright_      | Copyright      | 底部版本信息                                         |
| list_page_shown | bool           | 是否在导航栏显示“列表”菜单栏                         |
| paginate_by     | Option[int]    | 列表页中每页包含的项数目，设置为None表示不分页       |
| list_layout     | 'grid'/ 'list' | 列表页中按列表方式或者网格方式显示                   |

> 如果参数或变量和python内置函数的名称相同，将在最后加下划线以示区分。



## 导航栏(Nav)

顶部导航栏是一个有二级菜单的导航功能，下列的菜单项默认已添加：

- 首页 `Menu(text='首页', slug='home', url=reverse_lazy('dje_home'))`
- 所有图表`Menu(text='所有图表', slug='list', url=reverse_lazy('dje_list'))` ，可以通过 list_page_shown 参数控制此项不显示

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

> 注意：使用django视图反向解析时必须使用 `reverse_lazy`，而不是 `reverse`，否则出现无法解析的异常。因为此时 site_obj 还未挂载到项目全局的 url 路由规则之中。



## 底部版权栏(Copyright)

`Copyright` 类用于初始化页面底部的版权文字。可以传入的参数有：

- start_year：开始的年份
- powered_by: 版权主题名称

例子 `Copyright(start_year=2017, powered_by='Django-Echarts')` 的将渲染为下列文字：

```
©2017-2022, Powered By Django-Echarts
```



## 模板变量

各个子页面均继承自 `DJESiteBaseView` ，页面渲染时向模板传入下列数据。

| 特性     | 模板              | 变量名称   | 类型                        | 说明         |
| -------- | ----------------- | ---------- | --------------------------- | ------------ |
| 基础逻辑 | {theme}/base.html | site_title | `str`                       | 网站标题     |
|          |                   | theme      | `str`                       | 主题名称     |
|          |                   | nav        | `starter.widgets.Nav`       | 顶部导航栏   |
|          |                   | copyright  | `starter.widgets.Copyright` | 底部版权信息 |

