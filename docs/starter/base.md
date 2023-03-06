# 使用教程

## 一、 创建项目

### 1.1 Django&pyecharts版本

django-echarts 不会将 django 和 pyecharts 作为显式依赖库（虽然在代码中总是导入这两个库），对其版本没有强制性的依赖。下列是推荐性的版本。

| django-echarts版本系列 | pyecharts | echarts | django    | python |
| ---------------------- | --------- | ------- | --------- | ------ |
| 0.6.x                  | 1.9 - 2.0 | 5.4.1   | 2.0 - 4.1 | 3.7+   |
| 0.5.x                  | 1.9       | 4.8.0   | 2.0 - 4.1 | 3.7+   |

### 1.2 项目配置

在 Django 项目中，配置模块位于 *project.settings* 。和 django-echarts 有关的配置如下：

```python
BASE_DIR = Path(__file__).resolve().parent.parent

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
| STATICFILES_DIRS | 静态文件目录。                                               |
| DJANGO_ECHARTS   | django-echarts项目配置 <sup>2</sup>，字典类型。参数参见 `DJEOpts` 类。 |

1. 内置主题APP包括： django_echarts.contrib.bootstrap3 / django_echarts.contrib.bootstrap5 / django_echarts.contrib.material。
2. 默认配置已经能够支持最小化运行，此配置可以留空。

## 二、创建站点

### 2.1 初始化DJESite对象

> DJESite(site_title: str,  opts: Optional[SiteOpts] = None):

`DJESite` 是站点界面和逻辑的入口点，首先必须创建你自己的站点对象 `site_obj`。

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
| opts                 | SiteOpts     | 站点配置类                                                   |
| opts.nav_shown_pages | List         | 导航栏显示的菜单项，可选为 home / list /collection / settings。默认为 ['home'] <sup>1</sup> |

1. 此项设置必须在 `DJESite` 初始化时传入，以便将这些菜单项先插入导航栏靠前的位置

### 2.2 连接到项目路由模块

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

## 三、编写函数和注册echarts图表

### 3.1 新增图表

图表使用遵循“定义 - 注册 - 使用” 的规则。

`site_obj.register_chart` 装饰器用于注册图表的创建函数。默认未携带任何参数情况下，函数名将作为图表标识符。

```python
@site_obj.register_chart
def mychart():
    bar = Bar()
    # ...
    return bar
```

当然该装饰器也可以传入参数，这些参数用于构建对应的 `ChartInfo` 对象。

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

### 3.2 装饰器参数

装饰器 `DJESite.register_chart` 接受下列可选参数：

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
| **参数图表配置** |  |  |
| params_config | ParamConfig | 图表参数配置 <sup>2</sup> |
| **菜单参数** <sup>3</sup> |                |                                                |
| nav_parent_name     | str            | 上级菜单名称，默认为 catalog                   |
| nav_after_separator | bool           | 是否在菜单项前使用分隔符                       |

1. `Slug`类型指的是Django内置Converter，为符合正则表达式 `[-a-zA-Z0-9_]+` 的字符串，作为url的一部分。
1.  0.6新增。参见 [《参数化图表》](/guides/entity_params)
1.  在导航栏生成图表链接。从0.6.0开始，此项默认不启用，如需开启，需搭配 `DJESite.config_nav` 使用。

### 3.3 注册组件

> DJESite.register_html_widget(function=None, *, name: str = None)

装饰器 register_html_widget 用于注册HTML组件。

以注册ValuesPanel为例子。

```python
from datetime import date
from django_echarts.entities import ValuesPanel, ValueItem
from myapp import models

@site_obj.register_html_widget
def this_month_panel():
    today = date.today()
    number_p = ValuesPanel()
    access_total = models.AccessRecord.objects.filter(
        create_time__year=today.year, create_time__month=today.month
    ).count()
    item = ValueItem(access_total, f'{today.year}年{today.month}月访问量', '人次')
    number_p.add_widget(item)
    return number_p
```

## 四、网站配置

### 4.1 导航栏(Nav)

参见 [导航栏](starter/site_configuration)一章。

## 五、页面配置

### 5.1 首页

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

#### 5.1.1 大标题图表(JumbotronChart)

可以为 add_widgets 的 jumbotron_chart 指定一个图表名称，则显示该图表，不再显示 Jumbotron 组件。下面是一个例子：

```python
site_obj.add_widgets(jumbotron_chart='mychart')

@site_obj.register_chart(description='柱形图示例', catalog='示例一', top=2)
def mychart():
    bar = Bar()
    # ...
    return bar
```

#### 5.1.2 热门图表

按照网格方式显示标记为 top 的图表。向装饰器 `register_chart` 的 top 参数指定一个大于0的数字即可（数字越小，越靠前显示）。

```python
@site_obj.register_chart(description='柱形图示例', catalog='示例一', top=2)
def mychart():
    bar = Bar()
    # ...
    return bar
```

### 5.2 列表页

#### 5.2.1 搜索

列表页支持关键字搜索，搜索范围有：图表标题、标签、描述文字。

#### 5.2.2 显示样式

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

#### 5.2.3 设置分页

> 定义: SiteOpts.paginate_by:Optional[int] = None

在site创建时传入 `paginate_by` 参数，指定每页需要显示的数目，默认不启用分页特性。

```python
site_obj = DJESite(
    site_title='图表可视化',
    opts=SiteOpts(paginate_by=10)
)
```

