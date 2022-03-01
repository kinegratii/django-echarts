# 使用教程

正如 *快速开始*  一节所提到的，django-echarts 提供了一个简单便捷的脚手架工具包，她负责处理底层的视图逻辑、URL路由、模板、前端界面及其之间的连结，你只需编写构建图表的pyecharts代码。

## 创建项目

### Django&pyecharts版本

django-echarts 不会将 django 和 pyecharts 作为显式依赖库（虽然在代码中总是导入这两个库），对其版本没有强制性的依赖。下列是推荐性的版本。

| django-echarts版本系列 | pyecharts | django | python | 备注       |
| ---------------------- | --------- | ------ | ------ | ---------- |
| 0.5.x                  | 1.9+      | 2.0+   | 3.7+   | 开发维护中 |

### 项目配置

Django项目的配置模块位于 *project.settings* 。

1. django-echarts 携带了模板标签函数，因此需要将 `django_echarts` 添加到 `INSTALLED_APPS` 列表。
2. django-echarts包含了模板文html件，因此需要开启 `APP_DIRS` 功能。

```python
INSTALLED_APPS = [
    #...
    'django_echarts',
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
}
```



## 创建站点

### 初始化DJESite对象

> DJESite(site_title: str, theme: str = 'bootstrap5', opts: Optional[SiteOpts] = None):

`DJESite` 是所有界面和逻辑的入口点，首先必须创建你自己的 site 对象。

```python
from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
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
| theme                | str          | 可设置bootstrap3 / bootstrap5 / material 及其调色主题<sup>1</sup> |
| opts                 | SiteOpts     | 选项类<sup>2</sup>                                           |
| opts.nav_shown_pages | List         | 导航栏显示的菜单项，可选为 home / list /collection。默认为 ['home'] <sup>3</sup> |

1. 详见 “UI框架和主题” 一章
2. `SiteOpts` 是一个使用 `@dataclasses.dataclass` 装饰的数据类，详细配置参见各页面相关功能配置。
3. 此项设置必须在 `DJESite` 初始化时传入，以便将这些菜单项先插入导航栏靠前的位置

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

`site_obj.register_chart` 装饰器用于注册返回图表的函数。默认未携带任何参数情况下，函数名将作为图表标识符。

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
2. 使用特殊标识 'none' 表示不显示

### 其他配置

`DJESite.register_chart` 接受下列可选参数：

| 参数名称            | 类型           | 说明                                           |
| ------------------- | -------------- | ---------------------------------------------- |
| **图文参数**       |                |                                                |
| info                | `ChartInfo` | 如果有设置此项，忽略后面单独的图表参数         |
| name                | str            | 图表标识符，如果不指定，将使用所装饰函数的名称 |
| title               | str            | 图表标题                                       |
| description         | str            | 描述                                           |
| catalog             | str            | 分类，如果设置，将在顶部导航栏使用下拉列表显示 |
| top                 | int            | 置顶标志，0表示不置顶，数值越小，越靠前。      |
| tags                | List[str]      | 标签列表，列表搜索功能时，标签也是搜索范围。   |
| layout              | str            | 布局参数，参见 “组件和布局” 一章               |
| **菜单参数**        |                |                                                |
| nav_parent_name     | str            | 上级菜单名称，默认为 catalog                   |
| nav_after_separator | bool           | 是否在菜单项前使用分隔符                       |

## 注册HTML组件

### 注册组件

> DJESite.register_widget(function=None, *, name: str = None)

装饰器 register_widget 用于注册HTML组件。可支持的组件类型：

- Copyright / Jumbotron / Message
- ValuesPanel

以注册ValuesPanel为例子。

```python
@site_obj.register_widget
def this_month_panel():
    today = date.today()
    number_p = ValuesPanel(col_item_num=4)
    access_total = models.Record.objects.filter(
        create_time__year=today.year, create_time__month=today.month
    ).count()
    number_p.add(ValueItem(access_total, f'{today.year}年{today.month}月访问量', '人次'))
    return number_p
```

### 获取组件

> DJESite.widgets.get(name:str)

在注册组件后，可以通过标识获取到这个组件，如果是装饰器方式注册，每次将重新生成新的组件对象。

```python
number_p = site_obj.widgets.get('this_month_panel') # 每次重新生成新的 ValuesPanel 对象。
print(number_p.col_item_num) # 4
print(number_p[0].description) # '2022年1月访问量'
```



## 配置网站组件

### 导航栏(Nav)

导航栏位于页面顶部，由 左侧二级菜单 和 右侧 一级菜单 两部分组成，可以通过调用 DJESite 的方法添加连接。

| 函数                                                     | 说明                         |      |
| -------------------------------------------------------- | ---------------------------- | ---- |
| `DJESite.add_left_link(item: LinkItem, menu_title: str)` | 在左侧添加一级菜单           |      |
| `DJESite.add_left_link(item: LinkItem, menu_title: str)` | 在menu_title之下添加二级菜单 |      |
| `DJESite.add_right_link(item: LinkItem)`                 | 在右侧添加链接               |      |

下列的菜单项默认已添加到左侧菜单栏，可以通过设置 SiteOpts.nav_shown_pages 参数控制是否显示这些项目：

- 首页 `Menu(text='首页', slug='home', url=reverse_lazy('dje_home'))`
- 所有图表`Menu(text='所有图表', slug='list', url=reverse_lazy('dje_list'))` ，可以通过 list_page_shown 参数控制此项不显示

也可以通过 `DJESite` 提供的方法添加自定义链接。

```python
from django.urls import reverse_lazy
from django_echarts.starter.widgets import LinkItem

# 在右侧添加项目仓库链接，以新标签页方式打开
item = LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True)
site_obj.add_right_link(item)

item2 = LinkItem(text='关于', url=reverse_lazy('about'))
site_obj.add_right_link(item2)
```

类 `LinkItem` 表示一个超链接，url可以设置链接文本，也可以使用视图名称反向解析。

> 注意：使用django视图反向解析时必须使用 `reverse_lazy`，而不是 `reverse`，否则出现无法解析的异常。因为此时 site_obj 还未挂载到项目全局的 url 路由规则之中。

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

## 页面：首页

在首页可以通过 `add_widgets` 函数定制部分组件。

```
DJESite.add_widgets(*, jumbotron: Jumbotron = None, copyright_: Copyright = None, jumbotron_chart: str = None)
```

可支持的组件有：

| 参数/组件标识/模板变量名称 | 实际组件类型   | 引用方式              |
| -------------------------- | -------------- | --------------------- |
| home_jumbotron             | Jumbotron      | 静态<sup>1</sup>      |
| home_jumbotron_chart       | JumbotronChart | 静态/动态<sup>2</sup> |
| home_values_panel          | ValuesPanel    | 静态/动态             |

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

## 页面：列表页

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

