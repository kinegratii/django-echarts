# 使用教程

## 创建项目

### Django&pyecharts版本

django-echarts 不会将 django 和 pyecharts 作为显式依赖库（虽然在代码中总是导入这两个库），对其版本没有强制性的依赖。下列是推荐性的版本。

| django-echarts版本系列 | pyecharts | django | python | 备注       |
| ---------------------- | --------- | ------ | ------ | ---------- |
| 0.5.x                  | 1.9+      | 2.0+   | 3.7+   | 开发维护中 |

### 项目配置

在 Django 项目中，配置模块位于 *project.settings* 。和 django-echarts 有关的配置如下：

```python
INSTALLED_APPS = [
    #...
    'django_echarts',
    'django_echarts.contrib.bootstrap5'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # ...
        },
    },
]
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static').replace('\\', '/'),)
DJANGO_ECHARTS = {
    # ...
    'theme_name': 'bootstrap5.yeti'
}
```

配置项说明表

| 配置项           | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| INSTALLED_APPS   | 项目所包含的APP。必须包含 `django_echarts`和对应的主题APP <sup>1</sup>。 |
| TEMPLATES        | 模板引擎、文件目录。采用django引擎渲染，且必须开启 `APP_DIRS` 选项。 |
| STATIC_URL       | 静态文件URL。                                                |
| STATICFILES_DIRS | 静态文件目录。如无重写模板文件，可不配置。                   |
| DJANGO_ECHARTS   | django-echarts项目配置 <sup>2</sup>，字典类型。参数参见 `DJEOpts` 类。 |

1. 主题APP内置包括： django_echarts.contrib.bootstrap3 / django_echarts.contrib.bootstrap5 / django_echarts.contrib.material。
2. 默认配置已经能够支持最小化运行，可不配置此项。

## 创建站点

### 初始化DJESite对象

> DJESite(site_title: str,  opts: Optional[SiteOpts] = None):

`DJESite` 是所有界面和逻辑的入口点，首先必须创建你自己的站点对象 `site_obj`。

```python
from django_echarts.entities import Jumbotron, Copyright, LinkItem
from django_echarts.starter.sites import DJESite, SiteOpts

site_obj = DJESite(
    site_title='图表可视化',
    opts=SiteOpts(
        list_layout='grid',
        nav_shown_pages=['home', 'collection'],
        paginate_by=10
    )
)

site_obj.add_widgets(
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts')
)
```

对象创建时，可以设置以下参数：

| 参数                 | 类型或可选值 | 描述                                                         |
| -------------------- | ------------ | ------------------------------------------------------------ |
| site_title           | str          | 网站标题                                                     |
| opts                 | SiteOpts     | 选项类                                                       |
| opts.nav_shown_pages | List         | 导航栏显示的菜单项，可选为 home / list /collection / settings。默认为 ['home'] <sup>1</sup> |

1. 此项设置必须在 `DJESite` 初始化时传入，以便将这些菜单项先插入导航栏靠前的位置

### 连接到路由模块

> DJESite.urls: list[Union[URLResolver, URLPattern]]

 `DJESite.urls` 是所有视图的路由配置，需要由使用者手动将其添加到项目主路由模块。

```python
from django.conf.urls import url, include
from django.urls import path

from myapp.site_views import site_obj

urlpatterns = [
    # Your urls
    path('', include(site_obj.urls))
]
```

## 注册echarts图表

### 新增图表

`site_obj.register_chart` 装饰器用于注册图表的创建函数。默认未携带任何参数情况下，函数名将作为图表标识符。

```python
@site_obj.register_chart
def mychart():
    bar = Bar()
    # ...
    return bar
```

当然也可以携带一些参数，这些参数通常和 `ChartInfo` 类参数意义相同。

```python
@site_obj.register_chart(description='词云示例', catalog='示例一')
def mychart():
    bar = Bar()
    # ...
    return bar
```

对于使用固定静态数据构建的图表，可以通过 `functools.lru_cache`  装饰器缓存 pyecharts 图表对象，以提高执行效率。

```python
from functools import lru_cache

@site_obj.register_chart(description='词云示例', catalog='示例一')
@lru_cache
def mychart():
    bar = Bar()
    # ...
    return bar
```

### 其他配置

`DJESite.register_chart` 接受下列可选参数：

| 参数名称            | 类型           | 说明                                           |
| ------------------- | -------------- | ---------------------------------------------- |
| **图文参数**       |                |                                                |
| info                | `ChartInfo` | 如果有设置此项，忽略后面单独的图表参数         |
| name                | Slug <sup>1</sup>            | 图表标识符，如果不指定，将使用所装饰函数的名称 |
| title               | str            | 图表标题                                       |
| description         | str            | 描述                                           |
| catalog             | str            | 分类，如果设置 |
| top                 | int            | 置顶标志，0表示不置顶，数值越小，越靠前。      |
| tags                | List[str]      | 标签列表，列表搜索功能时，标签也是搜索范围。   |
| layout              | str            | 布局参数，参见 “组件和布局” 一章               |
| **菜单参数** |                |                                                |
| nav_parent_name     | str            | 上级菜单名称，默认为 catalog                   |
| nav_after_separator | bool           | 是否在菜单项前使用分隔符                       |

1. `Slug`类型指的是Django内置Converter，为符合正则表达式 `[-a-zA-Z0-9_]+` 的字符串，作为url的一部分。

### 关联导航栏

下面是演示如何添加到导航菜单栏的。以 `chart.title = 'Chart1'` 为例子：

| chart.catalog | nav_parent_name | 说明                              |
| ------------- | --------------- | --------------------------------- |
| None(未设置)  | None(未设置)    | 不显示在菜单栏上                  |
| 'BarCharts'   | None(未设置)    | 显示，“BarCharts- Chart1”         |
| None(未设置)  | 'Menu1'         | 显示，“Menu - Chart1”             |
| 'BarCharts'   | 'Menu1'         | 显示 "Menu - Chart1" <sup>1</sup> |
| 任意          | 'self'          | 显示一级菜单<sup>2</sup>          |
| 任意          | 'none'          | 不显示<sup>3</sup>                |

1. 只要 catalog 和 nav_parent_name 至少一个有设置，均显示为二级菜单
2. 使用特殊标识 'self' 表示显示为一级菜单
3. 使用特殊标识 'none' 表示不显示



## 注册HTML组件

### 注册组件

> DJESite.register_html_widget(function=None, *, name: str = None)

装饰器 register_html_widget 用于注册HTML组件。可支持的组件类型：

- Copyright / Jumbotron / Message
- ValuesPanel

以注册ValuesPanel为例子。

```python
from datetime import date
from django_echarts.entities import ValuesPanel
from myapp import models

@site_obj.register_html_widget
def this_month_panel():
    today = date.today()
    number_p = ValuesPanel(col_item_num=4)
    access_total = models.AccessRecord.objects.filter(
        create_time__year=today.year, create_time__month=today.month
    ).count()
    number_p.add(access_total, f'{today.year}年{today.month}月访问量', '人次')
    return number_p
```

### 获取组件

> DJESite.html_widgets.get(name:str)

在注册组件后，可以通过标识获取到这个组件，如果是装饰器方式注册，每次将重新生成新的组件对象。

```python
number_p = site_obj.html_widgets.get('this_month_panel')  # 每次重新生成新的 ValuesPanel 对象。
print(number_p.col_item_num)  # 4
print(number_p[0].description)  # '2022年1月访问量'
```

## 网站公共组件

### 导航栏(Nav)

导航栏位于页面顶部，由 *左侧二级菜单* 、 *右侧一级菜单* 和 *底部链接* 三部分组成，根据目标链接的类型有不同的添加方式。

**第一种：内置页面**

内置页面通常位于左侧二级菜单栏的最前面，使用 `SiteOpts.nav_shown_pages` 定义。

```python
SiteOpts(nav_shown_pages=['home', 'collection'])
```

包括：

| 标识       | 页面功能                                                     |
| ---------- | ------------------------------------------------------------ |
| home       | 首页。默认已添加。                                           |
| list       | 包含所有图表的信息页。不显示图表，显示描述、标签等。默认已添加。 |
| collection | 包含所有图表的合辑，显示图表和简短的文字描述信息。           |

**第二种：图表和合辑**

将图表或者合辑添加到左侧二级菜单，由 `DJESite.register_chart` / `DJESite.register_collection` 中参数控制 。详细参见 注册图表 一节。

**第三种：自定义链接**

> class LinkItem(text: str, url: str = None, slug: str = None, new_page: bool = False, after_separator: bool = False)

链接使用 `LinkItem` 类表示。

| 参数            | 类型 | 描述                                       |
| --------------- | ---- | ------------------------------------------ |
| text            | str  | 链接文字                                   |
| url             | str  | 链接地址                                   |
| slug            | str  | 标识符，可自动生成                         |
| new_page        | bool | target属性是否设置为 _blank                |
| after_separator | bool | 在菜单前是否添加分隔符，仅适用于顶部导航栏 |

**注意**：使用django视图反向解析时必须使用 `reverse_lazy`，而不是 `reverse`，否则出现无法解析的异常。因为此时 site_obj 还未挂载到项目全局的 url 路由规则之中。

`DJESite`提供了 `add_*_link` 函数用于向站点添加链接。

| 函数                                                     | 说明                         |      |
| -------------------------------------------------------- | ---------------------------- | ---- |
| `DJESite.add_left_link(item: LinkItem)`                  | 在左侧添加一级菜单           |      |
| `DJESite.add_left_link(item: LinkItem, menu_title: str)` | 在menu_title之下添加二级菜单 |      |
| `DJESite.add_right_link(item: LinkItem)`                 | 在右侧添加链接               |      |
| `DJESite.add_footer_link(item: LinkItem)`                 | 在底部添加链接               |      |

例子：

```python
from django.urls import reverse_lazy
from django_echarts.entities.html_widgets import LinkItem

# 在右侧添加项目仓库链接，以新标签页方式打开
item = LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True)
site_obj.add_right_link(item)

item2 = LinkItem(text='关于', url=reverse_lazy('about'))
site_obj.add_right_link(item2)
```

### 底部版权栏(Copyright)

`Copyright` 类用于初始化页面底部的版权文字。可以传入的参数有：

| 参数       | 类型 | 描述         |
| ---------- | ---- | ------------ |
| start_year | int  | 开始的年份   |
| powered_by | str  | 版权主题名称 |

例子 `Copyright(start_year=2017, powered_by='Django-Echarts')` 的将渲染为下列文字：

```
©2017-2022, Powered By Django-Echarts
```

## 首页

在首页可以通过 `add_widgets` 函数定制部分组件。

```
DJESite.add_widgets(*, jumbotron: Jumbotron = None, copyright_: Copyright = None, jumbotron_chart: str = None)
```

可支持的组件有：

| 参数/组件标识/模板变量名称 | 参数类型                 | 实际组件类型   |
| -------------------------- | ------------------------ | -------------- |
| copyright_                 | Copyright                | Copyright      |
| home_jumbotron             | Jumbotron  <sup>1</sup>  | Jumbotron      |
| home_jumbotron_chart       | Chart / str <sup>2</sup> | JumbotronChart |
| home_values_panel          | ValuesPanel / str        | ValuesPanel    |

1. 静态方式：home_jumbotron_chart 直接指定一个图表对象（如Bar）。
2. 动态方式：home_jumbotron_chart 仅指定一个图表字符串标识，这些图表或组件通过 `register_chart` / `register_widget` 的方式注册。

### 大标题组件(Jumbotron)

`Jumbotron` 是大标题组件的数据类。

```python
site_obj.add_widgets(
    jumbotron=Jumbotron('图表可视化', main_text='这是一个由django-echarts-starter驱动的可视化网站。', small_text='版本1.0'),
)
```

可设置下列参数：

| 参数       | 类型 | 描述     |
| ---------- | ---- | -------- |
| title      | str  | 主标题   |
| main_text  | str  | 主要文字 |
| small_text | str  | 小文字   |

### 大标题图表(JumbotronChart)

可以为 add_widgets 的 jumbotron_chart 指定一个图表名称，则显示该图表，不再显示 Jumbotron 组件。下面是一个例子：

```python
site_obj.add_widgets(jumbotron_chart='mychart')

@site_obj.register_chart(description='柱形图示例', catalog='示例一', top=2)
def mychart():
    bar = Bar()
    # ...
    return bar
```

### 热门图表

按照网格方式显示标记为 top 的图表。向装饰器 `register_chart` 的 top 参数指定一个大于0的数字即可（数字越小，越靠前显示）。

```python
@site_obj.register_chart(description='柱形图示例', catalog='示例一', top=2)
def mychart():
    bar = Bar()
    # ...
    return bar
```

## 列表页

### 搜索

列表页支持关键字搜索，搜索范围有：图表标题、标签、描述文字。

### 显示样式

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

