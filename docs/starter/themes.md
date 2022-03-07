# UI框架和主题

界面主题包括UI主题和调色，一个主题(Theme)可以设置不同的调色(Palette)。

主题资源包括：模板文件、静态文件和标签函数三个部分，并且以 Django App 的形式加载到项目之中。

```python
DJANGO_ECHARTS = {
    'theme_name':'bootstrap5.foo',
    'theme_app': 'django_echarts.contrib.bootstrap5',
    'theme_d2u': {
        'bootstrap5.foo': {
            'palette_css': '/static/bootstrap5/bootstrap5.foo.min.css'
        }
    }
}
```



## 配置主题

有关主题的配置选项均位于项目的 *settings.py* 模块。

- 完整的配置：

```python

INSTALLED_APPS = [
    # ...
    'django_echart',
    'django_echarts.contrib.bootstrap5'
]

DJANGO_ECHARTS = {
    'theme_name': 'bootstrap5',
    'theme_app': 'django_echarts.contrib.bootstrap5'
}
```

* 如果使用该主题默认的调色，则可以不设置 `theme_name`  和 `theme_app` 参数。

```python
INSTALLED_APPS = [
    # ...
    'django_echart',
    'django_echarts.contrib.bootstrap5'
]
```

* 使用不同的调色(palette)，格式为  `<UI框架>.<调色>` ：

```python
INSTALLED_APPS = [
    # ...
    'django_echart',
    'django_echarts.contrib.bootstrap5'
]

DJANGO_ECHARTS = {
    'theme_name': 'bootstrap5.yeti'
}
```

* 使用本地部署

```python
INSTALLED_APPS = [
    # ...
    'django_echart',
    'django_echarts.contrib.bootstrap5'
]

DJANGO_ECHARTS = {
    'theme_name': 'bootstrap5.yeti#local'
}
```

## 可用的内置主题

django-echarts内置以下主题：

| INSTALLED_APP                     | DJEOpts.site_theme          | 文件                                                   |
| --------------------------------- | --------------------------- | ------------------------------------------------------ |
| django_echarts.contrib.bootstrap3 |                             |                                                        |
|                                   | bootstrap3                  | 在线引用                                               |
|                                   | bootstrap3.{PALETTES}       | 在线引用                                               |
|                                   | bootstrap3.{PALETTES}#local | 本地引用，需先通过 `download -t THEME` 命令下载到本地  |
| django_echarts.contrib.bootstrap5 |                             |                                                        |
|                                   | bootstrap5                  | 在线引用                                               |
|                                   | bootstrap5.{PALETTES}       | 在线引用                                               |
|                                   | bootstrap5.{PALETTES}#local | 本地引用，需先通过  `download -t THEME` 命令下载到本地 |
| django_echarts.contrib.material   |                             |                                                        |
|                                   | material                    | 在线引用                                               |
|                                   | material#local              | 本地引用，需先通过  `download -t THEME` 命令下载到本地 |

其中  PALETTES 可以是下列调色主题之一：

```python
BOOTSTRAP3_PALETTES = [
    "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "lumen", "paper",
    "readable", "sandstone", "simplex", "slate", "spacelab", "superhero", "united", "yeti",
]

BOOTSTRAP5_PALETTES = ["cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "litera", "lumen", "lux", "materia","minty", "morph", "pulse", "quartz", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab","superhero", "united", "vapor", "yeti", "zephyr",
            ]
```

具体效果可参见网站  [https://bootswatch.com/](https://bootswatch.com/) 。

## 新的调色

django-echarts还支持自定义UI框架的调色主题。

第一步，通过 info命令查看调色css文件需要放置的本地文件路径。

```text
PS E:\projects\zinc> python .\manage.py info -t bootstrap5.foo
[File #01] : Catalog: palette_css
        Remote Url: https://bootswatch.com/5/foo/bootstrap.min.css
        Static Url: /static/bootstrap5/bootstrap5.foo.min.css
        Local Path: E:\projects\zinc\static\bootstrap5/bootstrap5.foo.min.css
[File #02] : Catalog: font_css
        Remote Url: https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css
        Static Url: /static/bootstrap5/bootstrap-icons.min.css
        Local Path: E:\projects\zinc\static\bootstrap5/bootstrap-icons.min.css
[File #03] : Catalog: jquery_js
        Remote Url: https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js
        Static Url: /static/bootstrap5/jquery.min.js
        Local Path: E:\projects\zinc\static\bootstrap5/jquery.min.js
[File #04] : Catalog: main_js
        Remote Url: https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js
        Static Url: /static/bootstrap5/bootstrap.bundle.min.js
        Local Path: E:\projects\zinc\static\bootstrap5/bootstrap.bundle.min.js

```

第二步，将编译的css文件，修改文件名称，放在 palette_css 项对应的本地路径。

第三步，配置 `DJEOpts.site_theme` 参数，字典键表示主题标识符，必须符合`<UI框架>` 或者 `<UI框架>.<调色>`的格式。

```python
INSTALLED_APPS = [
    # ...
    'django_echarts',
    'django_echarts.contrib.bootstrap5'
]

DJANGO_ECHARTS = {
    'theme_name': 'bootstrap5.foo',
    'theme_d2u': {
        'bootstrap5.foo': {
            'palette_css': '/static/bootstrap5/bootstrap5.foo.min.css'
        }
    }
}
```

第三步，此时 `DJESite`的theme参数就可以指定你自定义的名称。

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

2 在 `DJANGO_ECHARTS` 配置，添加 `#local` 后缀。

```python
DJANGO_ECHARTS = {
    'theme_name': 'bootstrap5.cerulean#local'
}
```



## 自定义UI主题

django-echarts 支持以 django app 形式（或python包）创建主题。

```text
my_theme/
    __init__.py
    static/
    templates/
        base.html
        home.html
    templatetags/
        __init__.py
        dje_my_theme.py
```

一个完整的主题APP包括：

- 基于DTS的模板文件
- 标签函数
- 静态文件
