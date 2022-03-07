# 视图和模板

本节介绍了 django-echarts中主要的API信息，包括：

- 网站配置
- 视图
- 模板文件和变量
- 接口方法

## 网站架构

网站可视化提供了一种用户友好的前台界面（和django-admin后台管理界面相对应）。主要由以下几个页面组成：

| 功能页面 | 功能特性                                                 | 默认实现视图类         |      |
| -------- | -------------------------------------------------------- | ---------------------- | ---- |
| 基础页面 | 负责网站的整体布局、风格，组件包括头部导航栏、底部版权栏 | -                      |      |
| 首页     | 大标题、热门/推荐图表组件                                | DJESiteHomeView        |      |
| 列表页面 | 显示所有图表的基本信息，支持分页                         | DJESiteListView        |      |
| 图表页面 | 显示由echarts渲染的可交互图表                            | DJESiteChartSingleView |      |
| 关于页面 | 显示基本信息                                             | DJESiteAboutView       |      |
| 设置页面 | 编辑部分设置项                                           | DJESiteSettingsView    |      |

## 路由

DJESite 内置包含下列路由：

| 功能页面 | 路由                           | 视图类型 | 视图类                 | 视图名称          |
| -------- | ------------------------------ | -------- | ---------------------- | ----------------- |
| 首页     | `''`                           | 前端     | DJESiteHomeView        | dje_home          |
| 列表页面 | `'list/'`                      | 前端     | DJESiteListView        | dje_list          |
| 图表页面 | `'chart/<slug:name>/'`         | 前端     | DJESiteDetailView      | dje_detail        |
| 图表页面 | `'chart/<slug:name>/options/'` | 后端     | DJSiteChartOptionsView | dje_chart_options |
| 关于页面 | `'about/'`                     | 前端     | DJESiteAboutView       | dje_about         |
| 设置页面 | `settings/`                    | 后端     | DJESiteSettingsView    | dje_settings      |

注：后端视图类指的是返回 `TemplateResponse`的视图类，前端视图类指的是返回 `JsonResponse` 的视图类。

## 视图类

 `DJESiteBackendView` 和 `DJESiteFrontendView` 均直接继承自 `View`， 并共同实现了站点对象注入。

在视图方法中可以使用下列方式获取绑定的站点对象。

```python
class MyView(DJESiteBackendView):
    def get(self, request, *args, **kwargs):
        site = SiteInjectMixin.get_site_object()
        # ...
```



### 后端视图类

 `DJESiteBackendView` 是所有后端视图类的基类 ，对应的模板页面为 *base.html* ，具体的需要传入的变量字典参见下一节的“模板及其变量”。

### 前端视图类

`DJESiteFrontendxView` 是所有前端视图类的基类。

## 接口方法

所有可重写的接口方法均以 *dje_* 开头。

### DJESiteBackendView

```python
class DJESiteBackendView:
    def dje_init_page_context(self, context, site: 'DJESite') -> Optional[str]:
        pass
```

**dje_init_page_context**

实现基于 DJESite的模板渲染。

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

### DJESite

```python
class DJESite:
    def dje_get_current_theme(self, request, *args, **kwargs) -> Theme:
        """Get the theme for this request."""
        return self.theme

    def dje_get_urls(self) -> List:
        """Custom you url routes here."""
        pass
```

**dje_get_urls**

返回自定义的视图路由配置。

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
