# 配置

## 定义

django-echarts 遵循统一配置的原则，所有的配置均定义在项目配置模块一个名为 `settings.DJANGO_ECHARTS` 变量中，该变量可以指向

- 一个`dict`对象
- `django_echarts.core.settings_store.DJEOpts` 对象

例子( *settings.py*)

```python
DJANGO_ECHARTS = {
    'echarts_version': '4.8.0',
    'dms_repo': 'pyecharts'
}

# 或者

from django_echarts.core.dms import DJEOpts

DJANGO_ECHARTS = DJEOpts(
    echarts_version='4.8.0',
    dms_repo='pyecharts',
)
```

## 依赖项

```python
DJEOpts.echarts_version: str = '4.8.0'
DJEOpts.dms_repo: str = 'pyecharts'
DJEOpts.dep2url: Dict[str, str]
```

关于依赖项的配置参见 “依赖项和静态文件” 一章。

## 图表渲染配置

这些配置默认不提供有效值，由各图表对象自行设置。如果这些配置有设置，则使用该配置覆盖各图表设置。

### 渲染引擎

```python
DJEOpts.render:str = ''
```

### ECharts主题

```python
DJEOpts.enable_echarts_theme:bool = False
```

django-echarts 支持 echarts 主题功能，为了减少主题资源加载，默认情况下不启用该功能。

- 全局配置：`enable_echarts_theme = False`
- 不会请求任何theme对应的javascript文件
- 前端 `echarts.init` 函数不传入任何主题参数，即使 python代码`pycharts.options.InitOpts` 传入了 `theme` 参数

## 脚手架

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

在使用按照图表下载依赖项时需要设置此项功能。

