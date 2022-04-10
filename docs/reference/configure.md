# 配置

## 定义

django-echarts 遵循统一配置的原则，所有的配置均定义在项目配置模块一个名为 `settings.DJANGO_ECHARTS` 变量中，该变量指向一个`dict`对象。

例子( *settings.py*)

```python
DJANGO_ECHARTS = {
    'echarts_version': '4.8.0',
    'dms_repo': 'pyecharts'
}
```

## 配置选项 DJEOpts

### 依赖项

```python
DJEOpts.echarts_version: str = '4.8.0'
DJEOpts.dms_repo: str = 'pyecharts'
DJEOpts.dep2url: Dict[str, str]
```

关于依赖项的配置参见 “依赖项和静态文件” 一章。

### 渲染引擎

这些配置默认不提供有效值，由各图表对象自行设置。如果这些配置有设置，则使用该配置覆盖各图表设置。

```python
DJEOpts.render:str = 'canvas'
```

可选值：canvas 或 svg。

### Echarts主题

```python
DJEOpts.echarts_theme:Option[str] = None
```

echarts主题全局性设置。

- 设置为`None`，使用各图表单独的设置。
- 设置为不为空的字符串，使用同一的设置。

### 主题名称

```
DJEOpts.theme_name:Optional[str] = '<?INSTALLED_APP>'
```

必填选项。默认为 `INSTALLED_APP` 对应主题的默认调色。

可以选择下列格式：

```python
theme_names = [
    'bootstrap3',
    'bootstrap3.flaty',
    'bootstrap5.simple#local'
]
```

参见 *UI框架和主题* 一节。

### 主题模块

```
DJEOpts.theme_app:Optional[str] = '?'
```

必填选项。主题APP包导入全路径，默认从 `INSTALLED_APPS` 中读取。

### 设置站点引用

```python
DJEOpts.site_class:Option[str] = None
```

django-echarts 默认不提供一个实例化 `DJESite`的对象，因此在使用某些非django框架入口的功能时，需要用户指定该站点对象的位置，即变量路径。该路径通常以项目内的app包名称为开头。

```python
DJANGO_ECHARTS = {
    'site_class': 'ccs.site_views.site_obj'
}
```

## 全局配置访问入口 SettingsStore

模块变量 `django_echarts.conf.DJANGO_ECHARTS_SETTINGS` 是项目配置的访问入口，是一个 `SettingsStore` 类实例。

```python
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
print(DJANGO_ECHARTS_SETTINGS.opts.dms_repo)
```

不正确的用法

```python
from django.conf import settings
print(settings.DJANGO_ECHARTS['dms_repo'])
```

### opts

属性，类型 `DJEOpts`。运行所使用的配置，由用户自定义和默认配置合并而成。

### dependency_manager

属性，类型 `DependencyManager`。 依赖项管理接口类。

### theme_manager

属性，类型 `ThemeManager`。主题管理接口类。

### theme

属性，类型 `Theme`。 当前所使用的主题。

### resolve_url

```python
def SettingsStore.resolve_url(dep_name:str, repo_name:Optional[str]=None)->str
```

实例方法。获取某个依赖项的实际url地址。

### get_site_obj

实例方法。根据 `DJEOpts.site_class` 获取对应的站点对象。

### switch_palette

```python
def SettingsStore.switch_palette(self, theme_label: str) -> Theme
```

实例方法。切换主题，修改 `SettingsStore.theme` 值。

## 依赖项接口类 DependencyManager

使用 `DJANGO_ECHARTS_SETTINGS.dependency_manager` 获取项目的依赖项管理访问入口。

## 主题接口类 ThemeManager

使用 `DJANGO_ECHARTS_SETTINGS.theme_manager` 获取项目的主题管理访问入口。

### create_from_module

类方法，创建器函数。

### available_palettes

属性，类型 `list`。当前主题可用的调色。

```python
available_palettes = ['bootstrap5', 'bootstrap5.yeti', ...]
```

### create_theme

实例方法。根据设置创建 `Theme` 对象。

```python
tms = ThemeManager.create_from_module('django_echarts.contrib.bootstrap5')
theme = tms.create_theme('bootstrap5.yeti')
```

### table_css

实例方法，返回表格的css类。

## 主题对象 Theme

由 `ThemeManager` 创建。

### 属性列表

一个主题对象由以下三个参数唯一确定。

| 属性          | 类型 | 描述                           |
| ------------- | ---- | ------------------------------ |
| name          | str  | 主题名称，如bootstrap5。       |
| theme_palette | str  | 主题调色，如 bootstrap5.yeti。 |
| is_local      | bool | 是否本地主题。                 |

字符串表示法如 `{theme}.{palette}(#local)`，示例：

```
bootstrap5
bootstrap5.yeti
bootstrap5#local
bootstrap5.yeti#local

```

