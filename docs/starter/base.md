# 功能设置

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

## 总体设置

### 初始化站点

`DJESite` 是所有界面和逻辑的入口点，首先必须创建你自己的 site 对象。

```python
from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
from django_echarts.starter.sites import DJESite, DJESiteDetailView

site_obj = DJESite(site_title='图表可视化')

site_obj.add_widgets(
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts')
)
```

对象创建时，可以设置以下参数：

| 参数       | 类型或可选值 | 描述                                                         |
| ---------- | ------------ | ------------------------------------------------------------ |
| site_title | str          | 网站标题                                                     |
| theme      | str          | 内置 bootstrap3/bootstrap3.cerulean/bootstrap5/material四个主题 |
| opts       | SiteOpts     | 选项类                                                       |


> 如果参数或变量和python内置函数的名称相同，将在最后加下划线以示区分。



### 导航栏(Nav)

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



### 底部版权栏(Copyright)

`Copyright` 类用于初始化页面底部的版权文字。可以传入的参数有：

- start_year：开始的年份
- powered_by: 版权主题名称

例子 `Copyright(start_year=2017, powered_by='Django-Echarts')` 的将渲染为下列文字：

```
©2017-2022, Powered By Django-Echarts
```

## 首页

### 大标题组件(Jumbotron)

`Jumbotron` 是大标题组件的数据类。

```python
site_obj.add_widgets(
    jumbotron=Jumbotron('图表可视化', main_text='这是一个由django-echarts-starter驱动的可视化网站。', small_text='版本1.0'),
)
```

可设置下列参数

- title: 主标题
- main_text: 主要文字
- small_text: 小文字

### 热门图表

按照网格方式显示标记为 top 的图表。向装饰器 `register_chart` 的 top 参数指定一个大于0的数字即可（数字越小，越靠前显示）。

```python
@site_obj.register_chart(description='词云示例', catalog='示例一', top=2)
def mychart():
    bar = Bar()
    # ...
    return bar
```

## 列表页

### 显示方式

> 定义: SiteOpts.list_layout: Literal['grid', 'list'] = 'list'

支持 “列表”/“网格” 两种方式

```python
# 列表方式
site_obj = DJESite(
    site_title='图表可视化',
    opts=SiteOpts(list_layout='list')
)
# 网格 3x4
site_obj = DJESite(
    site_title='图表可视化',
    opts=SiteOpts(list_layout='grid')
)
```



### 设置分页

> 定义: SiteOpts.paginate_by:Optional[int] = None

在site创建时传入 `paginate_by` 参数，指定每页需要显示的数目，默认不启用分页特性。

```python
site_obj = DJESite(
    site_title='图表可视化',
    opts=SiteOpts(paginate_by=10)
)
```

## 图表详情页

### 新增图表

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
@site_obj.register_chart(description='词云示例', catalog='示例一')
def mychart():
    bar = Bar()
    # ...
    return bar
```

### register_chart

`DJESite.register_chart` 用于注册新的图表函数，接受下列可选参数：

| 参数名称    | 类型           | 说明                                           |
| ----------- | -------------- | ---------------------------------------------- |
| info        | `DJEChartInfo` | 如果有设置此项，忽略后面的单独参数             |
| name        | str            | 图表标识符，如果不指定，将使用所装饰函数的名称 |
| title       | str            | 图表标题                                       |
| description | str            | 描述                                           |
| top         | int            | 置顶标志，0表示不置顶，数值越小，越靠前。      |
| catalog     | str            | 分类，如果设置，将在顶部导航栏使用下拉列表显示 |
| tags        | List[str]      | 标签列表                                       |

## SiteOpts选项类

`SiteOpts` 是一个使用 `@dataclasses.dataclass` 装饰的数据类。

| 参数            | 类型或可选值   | 描述                                                 |
| --------------- | -------------- | ---------------------------------------------------- |
| list_nav_item_shown | bool           | 是否在导航栏显示“All”菜单栏                         |
| paginate_by     | Option[int]    | 列表页中每页包含的项数目，设置为None表示不分页       |
| list_layout     | 'grid'/ 'list' | 列表页中按列表方式或者网格方式显示                   |
