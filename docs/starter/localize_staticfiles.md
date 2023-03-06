# 依赖项(二)：本地化

## 概述

django-echarts 本身不携带任何静态文件，默认引用在线资源，这些资源包括：

- echarts库文件
- echarts地图文件
- echarts主题文件
- UI主题文件

django-echarts 提供了一系列命令下载到本地。

## 配置

静态资源本地化功能需要配置静态资源的相关参数，以下是按 “项目统一目录”方式的配置。

```python
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static').replace('\\', '/'),)
```

django-echarts 将远程资源下载保存到 `STATICFILES_DIRS` 指向的目录。

## 使用方法

### 帮助信息

django-echarts 提供了 info 和 download 两个命令。下面的帮助信息不包含继承自 django 的选项。

```text
E:\projects\zinc> python .\manage.py info -h
usage: manage.py info [-h] [--chart CHART [CHART ...]] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO] 

Show one or some dependency files.

optional arguments:
  -h, --help            show this help message and exit
  --chart CHART [CHART ...], -c CHART [CHART ...]
                        The name of chart.
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.

E:\projects\zinc> python .\manage.py download -h
usage: manage.py download [-h] [--chart CHART [CHART ...]] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO] [--force]

Download one or some dependency files from remote CDN to project staticfile dirs.

optional arguments:
  -h, --help            show this help message and exit
  --chart CHART [CHART ...], -c CHART [CHART ...]
                        The name of chart.
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.
  --force, -f
```



| 选项参数 | 说明                                              |
| -------- | ------------------------------------------------- |
| dep      | 可多次添加。依赖项名称。                          |
| chart    | 可多次添加。图表标识，即 `ChartInfo.name`。       |
| theme    | 主题名称，默认为 `INSTALLED_APPS` 指定的主题APP。 |

### 查看依赖项信息

查看某个依赖项的具体信息

```text
E:\projects\zinc>python manage.py info -d echarts
[Resource #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
```

每个项输出四行信息：

- 第一行：基本信息。
- 第二行：远程url路径。
- 第三行：页面html 标签（link/script） 引用的地址。
- 第四行：本地实际文件路径，文字颜色表示是否存在该文件。

查看多个依赖项的信息。

```text
E:\projects\zinc>python manage.py info -d echarts 福建
[Resource #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
[Resource #02] 福建; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/maps/fujian.js
        Static Url: /static/maps/fujian.js
        Local Path: E:\projects\zinc\static\maps\fujian.js
```

### 下载依赖项文件

下载一个或多个依赖项

```text
python manage.py download -d echarts fujian
```

## 使用示例

### 按主题

查看主题的文件信息。

```text
python manage.py info --theme bootstrap5
python manage.py info -t bootstrap5.yeti
```

下载主题的文件信息。

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

### 按依赖项

查看依赖项的文件信息，多个依赖项使用空格隔开。

```text
python manage.py info --dep echarts
python manage.py info -d echarts 福建 上海
```

下载依赖项的文件信息，多个依赖项使用空格隔开。

```text
python manage.py download --dep echarts
python manage.py download -d echarts 福建 上海
```

### 按照图表

> Updated in v0.5.1: 不再需要设置 `site_class` 值。

在使用本功能时，必须先设置 `DJEOpts.site_class` 的值，该值指向网站入口 DJESite 对象。

```python
DJANGO_ECHARTS = {'site_class':'ccs.site_views.site_obj'}
```

查看某个图表的依赖项文件信息。

```text
E:\projects\zinc> python .\manage.py info -c fj-map
[Resource #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
[Resource #02] 福建; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/maps/fujian.js
        Static Url: /static/maps/fujian.js
        Local Path: E:\projects\zinc\static\maps/fujian.js
```


## 
