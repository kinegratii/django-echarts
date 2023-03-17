# 网站配置

## 导航栏(Nav)

> Update in 0.6.0: 新增  `DJESite.config_nav` 函数。

网站导航栏包括：左侧导航栏、右侧导航栏、底部导航栏，其中左侧、右侧（均位于顶部）支持下拉菜单，底部导航栏仅支持多个链接形式。

有两种使用方法。

## SiteOptions.nav_shown_pages

```python
class SiteOpts:
    """The opts for DJESite."""
    # ...
    nav_shown_pages: List = field(default_factory=lambda: ['home'])
```

该属性在 `DJESite` 对象初始化的时候传入，`nav_shown_pages` 为包含表示特定页面标识（字符串）的列表，可选的有：home / list / collection / settings / chart_nav 。

其中chart_nav需调用 `DJESite.config_nav`。

## 函数config_nav

```python
DJESite.config_nav(self, menu_config: dict = None)
```

函数`config_nav` 用于配置导航栏，需注意两点：

- 该函数是一次性配置的，将覆盖 `SiteOptions.nav_shown_pages`的配置。
- 该函数必须在所有 `register_chart` 之后调用，一般在 `urls`模块调用。

`menu_config` 参数基本形式如下：

```python
class NavConfig(TypedDict):
    nav_left: NotRequired[List[Union[str, dict]]]
    nav_right: NotRequired[List[Union[str, dict]]]
    nav_footer: NotRequired[List[Union[str, dict]]]
```

一个菜单项可以是以下几种形式：

- 内置页面(str)：home / list / collection / settings
- 图表分类导航(str)：chart_nav
- 图表或合辑资源标识符(str)：使用其URI字符串形式
- django视图链接(str)：使用视图名称及其参数
- 自定义链接(dict)：适用于菜单或菜单项

### 1 自定义链接

这是最为基础的定义形式，完整的链接定义如下：

```python
{'text': '网站源码', 'slug':'site_source', 'url': 'https://github.com/kinegratii/zinc', 'new_page': True}
```

| 属性     | 描述                               |
| -------- | ---------------------------------- |
| text     | 必选，链接文字。                   |
| url      | 必选，链接。                       |
| slug     | 可选，标识符，默认生成uuid字符串。 |
| new_page | 可选，默认为False。                |

### 2 菜单定义

```python
{'text': '网站源码', 'slug':'site_source', 'children':[...]}
```

使用键 `children` 表明这是一个菜单列表，下级菜单定义在属性children之中。

### 3 内置页面

可支持的内置页面如下：

| 标识符     | 页面       |
| ---------- | ---------- |
| home       | 首页       |
| list       | 图表列表页 |
| collection | 合辑列表页 |
| settings   | 设置页面   |

### 3 Django视图

```python
{'text':'大屏面板', 'view_name': 'dashbord', 'args':[], 'kwargs':{}，'new_page':False}
```

使用 `reverse_lazy` 反向解析url。

### 4 图表资源

```python
{'text': '2020年数据', 'slug':'family_type_2020', 'url': 'chart:yearly_family_types/year/2020', 'new_page': False}
```

类似于

```python
{'text':'2020年数据', 'view_name': 'dje_chart_single', 'args':['yearly_family_types','/year/2020'], 'kwargs':{}，'new_page':False}
```



### 5 图表分类导航chart_nav

```python
'chart_nav'
```

该字符串仅为占位符，函数 `DJESite.config_nav` 将根据 `register_chart` 的 catalog，在该位置添加菜单栏。

该配置仅可用于左侧导航栏。

## 配置示例

### 默认配置

默认配置（不调用 `config_nav`函数），仅包含 `nav_shown_pages`所定义菜单。

### 0.5兼容配置

以下是 django-echart 0.6 兼容0.5版本的配置方法：

```python
site_obj = DJESite(title='示例站点', opts=SiteOpts(nav_shown_pages=['home', 'list', 'chart_nav']))


@site_obj.register(..., catalog='菜单1')
def chart_1():
    pass


site_obj.config_nav()
```

### 常规配置

```python
nav = {
    'nav_left': ['home', 'list', 'chart_nav', {'text': '2020年数据', 'url': 'chart:yearly_family/year/2020'}],
    'nav_right': ['settings'],
    'nav_footer': [
        {'text': '福建统计年鉴2021', 'url': 'https://tjj.fujian.gov.cn/tongjinianjian/dz2021/index.htm', 'new_page': True},
        {'text': '网站源码', 'url': 'https://github.com/kinegratii/zinc', 'new_page': True},
    ]
}
```



### 关联导航栏

下面是演示如何添加到导航菜单栏的。以 `chart.title = 'Chart1'` 为例子：

| chart.catalog | nav_parent_name | 说明                              |
| ------------- | --------------- | --------------------------------- |
| None(未设置)  | None(未设置)    | 不显示在菜单栏上                  |
| 'BarCharts'   | None(未设置)    | 显示，“BarCharts- Chart1”         |
| None(未设置)  | 'Menu'          | 显示，“Menu - Chart1”             |
| 'BarCharts'   | 'Menu'          | 显示 "Menu - Chart1" <sup>1</sup> |
| 任意          | 'self'          | 显示一级菜单<sup>2</sup>          |
| 任意          | 'none'          | 不显示<sup>3</sup>                |

1. 只要 catalog 和 nav_parent_name 至少一个有设置，均显示为二级菜单
2. 使用特殊标识 'self' 表示显示为一级菜单
3. 使用特殊标识 'none' 表示不显示
