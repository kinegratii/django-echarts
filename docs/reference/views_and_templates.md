# 视图和模板

本节介绍了 `django_echarts` 业务层 中主要的API信息，包括视图、模板、接口方法。涉及到的代码包：

| 包/模块                     | 描述                    |
| --------------------------- | ----------------------- |
| django_echarts.starter      | 一个可视化网站脚手架    |
| django_echarts.ajax_echarts | ajax方式渲染echarts图表 |
| django_echarts.geojson      | 处理geojson数据         |

## 路由与视图

django_echarts 包含下列路由：

| 功能页面                        | 路由                           | 视图类 <sup>1</sup>    | 视图名称          |
| ------------------------------- | ------------------------------ | ---------------------- | ----------------- |
| **django_echarts.starter**      |                                |                        |                   |
| 首页                            | `''`                           | DJESiteHomeView        | dje_home          |
| 列表页面                        | `'list/'`                      | DJESiteListView        | dje_list          |
| 图表页面                        | `'chart/<slug:name>/'`         | DJESiteDetailView      | dje_detail        |
| 关于页面                        | `'about/'`                     | DJESiteAboutView       | dje_about         |
| 设置页面                        | `settings/`                    | DJESiteSettingsView    | dje_settings      |
| **django_echarts.ajax_echarts** |                                |                        |                   |
| 图表options数据                 | `'chart/<slug:name>/options/'` | DJSiteChartOptionsView | dje_chart_options |
| **django_echarts.geojson**      |                                |                        |                   |
| geojson数据                     | `geojson/<str:geojson_name>`   | GeojsonDataView        | dje_geojson       |

1. 视图类可以通过 `DJESite.register_view` 替换为自己的视图类。
1. 后端视图类指的是返回 `TemplateResponse`的视图类，前端视图类指的是返回 `JsonResponse` 的视图类。

## Starter网站架构

网站可视化提供了一种用户友好的前台界面（和django-admin后台管理界面相对应）。主要由以下几个页面组成：

| 功能页面 | 功能特性                                                 | 默认实现视图类         |      |
| -------- | -------------------------------------------------------- | ---------------------- | ---- |
| 基础页面 | 负责网站的整体布局、风格，组件包括头部导航栏、底部版权栏 | -                      |      |
| 首页     | 大标题、热门/推荐图表组件                                | DJESiteHomeView        |      |
| 列表页面 | 显示所有图表的基本信息，支持分页                         | DJESiteListView        |      |
| 图表页面 | 显示由echarts渲染的可交互图表                            | DJESiteChartSingleView |      |
| 关于页面 | 显示基本信息                                             | DJESiteAboutView       |      |
| 设置页面 | 编辑部分设置项                                           | DJESiteSettingsView    |      |



## 站点对象DJESite

### 构造函数

```python
class DJESite(site_title: str, opts: Optional[SiteOpts] = None)
```

参数可传入标题和配置类，如果未指定配置对象，则采用默认配置。

### opts

属性。返回配置对象。

### urls

属性。路由列表。需使用 `include` 挂载到项目主路由模块。

### register_view

使用自己视图类替换现有内置视图。

### config_nav

配置导航栏。

### add_left_link

> Removed in 0.6.0

添加到左侧导航栏。

```python
# 添加为一级菜单
site_obj.add_left_link(item=LinkItem(...)) 

# 在一级菜单“Menu1”之下添加二级菜单
site_obj.add_left_link(item=LinkItem(...), menu_title='Menu1') 
```

### add_footer_link

> Remove in 0.6.0

添加底部链接。

```python
site_obj.add_footer_link(item=LinkItem(...)) 
```

### add_widgets

添加组件。

### register_chart

函数，可作为装饰器。注册一个图表。

### register_html_widget

函数，可作为装饰器。注册一个HTML组件。

### register_collection

函数，可作为装饰器。注册合辑页面。

### extend_urlpatterns

新增自定义的视图路由配置。确保在挂载到项目主路由模块之前调用。

## 站点配置



```python
@dataclass
class SiteOpts:
    """The opts for DJESite."""
    list_layout: Literal['grid', 'list'] = 'grid'
    paginate_by: Optional[int] = 0
    nav_top_fixed: bool = False
    detail_tags_position: Literal['none', 'top', 'bottom'] = 'top'
    detail_sidebar_shown: bool = True
    nav_shown_pages: List = field(default_factory=lambda: ['home'])
```

配置项如下：

| 参数                 | 页面   | 描述                 |
| -------------------- | ------ | -------------------- |
| nav_top_fixed        | 总体   | 是否固定顶部导航栏   |
| nav_shown_pages      | 总体   | 导航栏默认显示的页面 |
| list_layout          | 列表页 | 每项的布局           |
| paginate_by          | 列表页 | 每页的项目数目       |
| detail_tags_position | 图表页 | 标签位置             |
| detail_sidebar_shown | 图标页 | 是否显示左侧导航栏   |



## 视图类

### SiteInjectMixin

 `DJESiteBackendView` 和 `DJESiteFrontendView` 均直接继承自 `View`， 并共同实现了站点对象注入。

在视图方法中可以使用下列方式获取绑定的站点对象。

```python
class MyView(DJESiteBackendView):
    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        # ...
```

### DJESiteBackendView

 `DJESiteBackendView` 是所有后端视图类的基类 ，对应的模板页面为 *base.html* ，具体的需要传入的变量字典参见下一节的“模板及其变量”。

### DJESiteFrontendxView

`DJESiteFrontendxView` 是所有前端视图类的基类。

所有可重写的接口方法均以 *dje_* 开头。

### DJESiteBackendView

```python
class DJESiteBackendView(TemplateResponseMixin, ContextMixin, SiteInjectMixin, View):
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        pass
```

**dje_init_page_context**

已废弃。实现基于 DJESite的模板渲染。

目前可以按照 `TemplateView` 方式自定义自己的视图类。

```python
class MyPageView(DJESiteBackendView):
    
    template_name = 'mypage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'John'
        return context
```



### DJESiteAjaxView

```python
class DJESiteAjaxView(View):
    def dje_get(self, request, *args, **kwargs) -> Any:
        pass

    def dje_post(self, request, *args, **kwargs) -> Any:
        pass
```

**dje_get**

**dje_post**

处理Ajax请求的基础类，并实现以下特性：

- 可以通过 `kwargs.get('site')` 获取当前绑定的DJESite对象。
- 直接返回 list 或者 dict 对象即可，无需直接返回 `JSONResponse`。



## 模板及其变量

### 基础页(Base)

| 模板              | 变量名称   | 类型                                       | 说明         |
| ----------------- | ---------- | ------------------------------------------ | ------------ |
| base.html | page_title | `str`                                      | 网站标题     |
|                   | opts       | `django_echarts.starter.sites.SiteOpts`    | 选项对象     |
|                   | nav        | `django_echarts.starter.widgets.Nav`       | 顶部导航栏   |
|                   | copyright  | `django_echarts.starter.widgets.Copyright` | 底部版权信息 |

其他模板页面均继承 *base.html* 。

### 基础页Block

| Block名称      | 作用                  | 默认使用的变量或标签函数 |
| -------------- | --------------------- | ------------------------ |
| include_css    | css样式，             | theme / theme_css        |
| extra_css      | 扩展css，由子页面重写 | 无                       |
| nav            | 导航栏                | nav / opts               |
| main_content   | 主界面                |                          |
| include_script | 公共js                | theme / theme_js         |
| extra_script   | 扩展js，由子页面重写  |                          |

### 主页(Home)

| 模板              | 变量名称            | 类型                        | 说明               |
| ----------------- | ------------------- | --------------------------- | ------------------ |
| home.html | jumbotron           | `starter.widgets.Jumbotron` | 大标题             |
|                   | top_chart_info_list | `List[ChartInfo]`        | 热门推荐的图表信息 |

### 列表页(List)

根据是否具有分页特性，使用不同的模板文件，并传入不同模板变量。

**无分页**

| 模板              | 变量名称        | 类型                 | 说明                                     |
| ----------------- | --------------- | -------------------- | ---------------------------------------- |
| list.html | chart_info_list | `List[ChartInfo]` | 图表的基本信息，包括标题、标识、介绍文本 |


**有分页**

| 模板                             | 变量名称         | 类型                         | 说明                           |
| -------------------------------- | ---------------- | ---------------------------- | ------------------------------ |
| list_with_paginator.html | page_obj         | `django.core.paginator.Page` | django构建的分页对象。         |
|                                  | elided_page_nums | List[Union[int, str]]        | 省略形式的页码列表。                   |

说明：

- 可以通过 `page_obj.object_list` 访问具体的条目数据，类型与无分页的 `chart_info_list`，其他属性可以参见 [《Django Paginator 》](https://docs.djangoproject.com/en/4.0/topics/pagination/)。

### 详情页(Detail)

根据是否存在对应的图表，显示不同的模板。

**有图表**

| 模板                | 变量名称   | 类型                                          | 说明                                     |
| ------------------- | ---------- | --------------------------------------------- | ---------------------------------------- |
| detail.html | menu       | `List[ChartInfo]`                          | 图表的基本信息，包括标题、标识、介绍文本 |
|                     | chart_info | `django_echarts.core.charttools.ChartInfo` | 图表基本信息                             |
|                     | chart_obj  | `pycharts.charts.Base`                        | 图表对象。                               |

**无图表**

| 模板               | 变量名称 | 类型 | 说明 |
| ------------------ | -------- | ---- | ---- |
| empty.html | -        | -    | -    |

### 关于页(About)



| 模板               | 变量名称 | 类型 | 说明 |
| ------------------ | -------- | ---- | ---- |
| about.html | -        | -    | -    |

### 消息页(Message)

| 模板                 | 变量名称 | 类型 | 说明     |
| -------------------- | -------- | ---- | -------- |
| message.html | message  | str  | 消息文字 |

### 设置页(Settings)

| 模板          | 变量名称 | 类型         | 说明         |
| ------------- | -------- | ------------ | ------------ |
| settings.html | form     | SiteOptsForm | 配置表单对象 |
