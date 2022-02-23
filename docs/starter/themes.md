# UI框架和主题

界面主题包括UI框架和调色主题。

## 内置主题

django-echarts内置以下主题：

| 标识符                      | 文件                                                   |
| --------------------------- | ------------------------------------------------------ |
| bootstrap3                  | 在线引用                                               |
| bootstrap3.{PALETTES}       | 在线引用                                               |
| bootstrap3.{PALETTES}#local | 本地引用，需先通过 `download -t THEME` 命令下载到本地  |
| bootstrap5                  | 在线引用                                               |
| bootstrap5.{PALETTES}       | 在线引用                                               |
| bootstrap5.{PALETTES}#local | 本地引用，需先通过  `download -t THEME` 命令下载到本地 |
| material                    | 在线引用                                               |

其中  PALETTES 可以是下列调色主题之一：

```python
BOOTSTRAP3_PALETTES = [
    "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "lumen", "paper",
    "readable", "sandstone", "simplex", "slate", "spacelab", "superhero", "united", "yeti",
]

BOOTSTRAP5_PALETTES = [
    "cerulea", "cosm", "cybor", "darkl", "flatl", "journa", "liter", "lume", "lu", "materi",
    "mint", "morp", "puls", "quart", "sandston", "simple", "sketch", "slat", "sola", "spacela",
    "superher", "unite", "vapo", "yet", "zephy",
]
```

具体效果可参见网站  [https://bootswatch.com/](https://bootswatch.com/) 。

## 本地化主题

为了简化自定义设置过程的繁琐操作，django-echarts提供了一个简便的命令行工具。

1 通过命令行下载文件。

```shell
$ python manage.py download --theme bootstrap5.cerulean
Download file bootstrap.min.css start!
Download file bootstrap-icons.min.css start!
Download file jquery.min.js start!
Download file bootstrap.bundle.min.js start!
File bootstrap-icons.min.css download success!
File bootstrap.bundle.min.js download success!
File jquery.min.js download success!
File bootstrap.min.css download success!
Task Completed! You can use "bootstrap5.cerulean#local" to the site config.
```

该命令将自动下载文件并保存在项目静态文件目录下，文件结构如下：

```
|-- static
     |-- bootstrap5
           |-- bootstrap5.cerulean.min.css
           |-- bootstrap-icons.min.css
           |-- jquery.min.js
           |-- bootstrap.bundle.min.js
```

2 在DJESite初始化方法的theme参数，添加 `#local` 后缀。

```python
site_obj = DJESite(
    site_title='图表可视化',
    theme='bootstrap5.cerulean#local',
    list_layout='grid'
)
```

## 自定义调色主题

django-echarts还支持自定义UI框架的调色主题。

准备你的css文件，修改文件名称，放在static目录下。

```text
|-- static
    |-- bootstrap3.foo.min.css
```



第二步，调用 `install_theme` 函数，字典键表示主题标识符，必须符合`<UI框架>` 或者 `<UI框架>.<调色>`的格式。

```python
from django_echarts.core.themes import install_theme

# 只覆盖palette_css对应文件，其他文件还是使用bootstrap3默认的文件

install_theme('bootstrap3.foo', {'palette_css': '/static/bootstrap3.foo.min.css'})

site_obj = DJESite(
    site_title='图表可视化',
    theme='bootstrap3.foo',
    list_layout='grid'
)
```

第三步，此时 `DJESite`的theme参数就可以指定你自定义的名称。


## 动态切换主题

根据用户的请求和设置为每一个请求指定特定的主题。以下是基于用户session设置切换主题。

```python
from django_echarts.starter.sites import DJESite
from django_echarts.core.themes import get_theme, Theme

class MySite(DJESite):
    
    def get_current_theme(self, request, *args, **kwargs):
        theme_name = request.session.get('theme')
        try:
            theme = get_theme(theme_name)
        except ValueError:
            theme = get_theme(self.theme)
        return theme
        
```



## 自定义UI框架

（此功能暂未实现.）

## 参考资料

- bootstrap3调色css: [ https://bootswatch.com/3/]( https://bootswatch.com/3/)
- materialcss: [https://materializecss.com/](https://materializecss.com/)