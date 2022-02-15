# API参考

本节介绍了每个模板的变量。

## 基本架构(Base)

 `DJESiteBaseView` 是所有视图类的基类 ，页面渲染时向模板传入下列数据。

| 模板              | 变量名称   | 类型                                       | 说明         |
| ----------------- | ---------- | ------------------------------------------ | ------------ |
| {theme}/base.html | site_title | `str`                                      | 网站标题     |
|                   | theme      | `django_echarts.core.themes.Theme`         | 主题名称     |
|                   | opts      | `django_echarts.starter.sites.SiteOpts`     | 选项对象     |
|                   | nav        | `django_echarts.starter.widgets.Nav`       | 顶部导航栏   |
|                   | copyright  | `django_echarts.starter.widgets.Copyright` | 底部版权信息 |

其他模板页面均继承 *{theme}/base.html* 。

## 路由

DJESite 内置包含下列路由：

| 路由                         | 视图类                 | 视图名称          |
| ---------------------------- | ---------------------- | ----------------- |
| ''                           | DJESiteHomeView        | dje_home          |
| 'list/'                      | DJESiteListView        | dje_list          |
| 'chart/<slug:name>/'         | DJESiteDetailView      | dje_detail        |
| 'chart/<slug:name>/options/' | DJSiteChartOptionsView | dje_chart_options |
| 'about/'                     | DJESiteAboutView       | dje_about         |

## 视图类与接口

可继承类重写的方法均以 *dje_* 开头。

### DJESiteBaseView

```python
class DJESiteBaseView:
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

处理Ajax请求的基础类。

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

**dje_get_current_theme**

返回基于当前用户请求的主题对象。

**dje_get_urls**

返回自定义的视图路由配置。

## 模板变量

### 主页(Home)

| 模板              | 变量名称            | 类型                        | 说明               |
| ----------------- | ------------------- | --------------------------- | ------------------ |
| {theme}/home.html | jumbotron           | `starter.widgets.Jumbotron` | 大标题             |
|                   | top_chart_info_list | `List[DJEChartInfo]`        | 热门推荐的图表信息 |

### 列表页(List)

根据是否具有分页特性，使用不同的模板文件，并传入不同模板变量。

**无分页**

| 模板              | 变量名称        | 类型                 | 说明                                     |
| ----------------- | --------------- | -------------------- | ---------------------------------------- |
| {theme}/list.html | chart_info_list | `List[DJEChartInfo]` | 图表的基本信息，包括标题、标识、介绍文本 |


**有分页**

| 模板                             | 变量名称         | 类型                         | 说明                           |
| -------------------------------- | ---------------- | ---------------------------- | ------------------------------ |
| {theme}/list_with_paginator.html | page_obj         | `django.core.paginator.Page` | django构建的分页对象。         |
|                                  | elided_page_nums | List[Union[int, str]]        | 页码列举。                   |

说明：

- 可以通过 `page_obj.object_list` 访问具体的条目数据，类型与无分页的 `chart_info_list`，其他属性可以参见 [《Django Paginator 》](https://docs.djangoproject.com/en/4.0/topics/pagination/)。

### 详情页(Detail)

根据是否存在对应的图表，显示不同的模板。

**有图表**

| 模板                | 变量名称   | 类型                                          | 说明                                     |
| ------------------- | ---------- | --------------------------------------------- | ---------------------------------------- |
| {theme}/detail.html | menu       | `List[DJEChartInfo]`                          | 图表的基本信息，包括标题、标识、介绍文本 |
|                     | chart_info | `django_echarts.core.charttools.DJEChartInfo` | 图表基本信息                             |
|                     | chart_obj  | `pycharts.charts.Base`                        | 图表对象。                               |

**无图表**

| 模板               | 变量名称 | 类型 | 说明 |
| ------------------ | -------- | ---- | ---- |
| {theme}/empty.html | -        | -    | -    |

### 关于页(About)



| 模板               | 变量名称 | 类型 | 说明 |
| ------------------ | -------- | ---- | ---- |
| {theme}/about.html | -        | -    | -    |

### 消息页(Message)

| 模板                 | 变量名称 | 类型 | 说明     |
| -------------------- | -------- | ---- | -------- |
| {theme}/message.html | message  | str  | 消息文字 |
