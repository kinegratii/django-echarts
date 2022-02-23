# 命令行工具

django-echarts 提供了一个包含若干个命令的 CLI 工具，这些命令都是标准的 Django 管理命令，均定义在 `django_echarts.management.commands` 包下。

本文档列出的帮助信息不包含继承自django命令的选项，你可以使用以下命令查看完整的帮助信息。

```shell
python manage.py <command> -h
```

## 静态文件 - 查看(info)和下载(download)

### 帮助信息

命令说明。

```text
E:\projects\django-echarts\example>python manage.py info -h
usage: manage.py info [-h] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO]

Show one or some dependency files.

optional arguments:
  -h, --help            show this help message and exit
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.
E:\projects\django-echarts\example>python manage.py download -h
usage: manage.py download [-h] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO] [--override]

Download one or some dependency files from remote CDN to project staticfile dirs.

optional arguments:
  -h, --help            show this help message and exit
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.
  --override, -o
```

备注

| 选项参数 | 说明                                        |
| -------- | ------------------------------------------- |
| dep      | 可多次添加。依赖项名称。                    |
| chart    | 可多次添加。图表标识，即 `ChartInfo.name`。 |
| theme    | 主题名称。                                  |



### 按主题

查看主题的文件信息。

```text
python manage.py info --theme bootstrap5
python manage.py info -t bootstrap5.yeti
```

下载主题的文件信息。

```text
python manage.py download --theme bootstrap5
python manage.py download -t bootstrap5.yeti
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

在使用本功能时，必须先设置 `DJEOpts.site_class` 的值，该值指向网站入口 DJESite 对象。

```python
DJANGO_ECHARTS = {'site_class':'ccs.site_views.site_obj'}
```

查看某个图表的依赖项文件信息。

```text
PS E:\projects\zinc> python .\manage.py info -c fj-map
[File #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
[File #02] 福建; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/maps/fujian.js
        Static Url: /static/maps/fujian.js
        Local Path: E:\projects\zinc\static\maps/fujian.js
```


## startsite - 生成视图代码

### 帮助信息

创建 初始化site的代码片段。

```text
E:\projects\django-echarts\example>python manage.py startsite -h
usage: manage.py startsite [-h] [--site-title SITE_TITLE] [--start-year START_YEAR] [--powered-by POWERED_BY]
                           [--override] output

Auto generate site_views.py file.

positional arguments:
  output                The output file.

optional arguments:
  -h, --help            show this help message and exit
  --site-title SITE_TITLE, -t SITE_TITLE
                        The title of site.
  --start-year START_YEAR, -y START_YEAR
                        The start year.
  --powered-by POWERED_BY, -p POWERED_BY
                        The principal of copyright.
  --override, -o
```

## starttpl - 生成模板文件

### 使用方法

```text
E:\projects\zinc> python .\manage.py starttpl -h
usage: manage.py starttpl [-h] [--tpl_name TPL_NAME [TPL_NAME ...]] [--all] [--override] 
                          {bootstrap3,bootstrap5,material}

Copy the builtin template files to your project template dir.

positional arguments:
  {bootstrap3,bootstrap5,material}
                        The name of theme.

optional arguments:
  -h, --help            show this help message and exit
  --tpl_name TPL_NAME [TPL_NAME ...], -n TPL_NAME [TPL_NAME ...]
                        The name list of template files.
  --all, -a             Whether copy files for this theme.
  --override, -o        Whether to copy if the file exists.
```

### 查看主题所有文件

查看bootstrap5主题的所有模板文件。

```text
E:\projects\zinc> python .\manage.py starttpl bootstrap5
The template names of Theme [bootstrap5]:
        about.html
        base.html
        detail.html
        detail_frontend.html
        home.html
        items_grid.html
        items_list.html
        list.html
        list_with_paginator.html
        message.html
```

### 复制模板文件

使用 `-n` 复制一个或多个文件，如果项目模板目录已经存在该文件，则需要添加 `-o` 覆盖，否则跳过复制。`-n` 的参数可以不添加后缀格式的 .html 。

```text
PS E:\projects\zinc> python .\manage.py starttpl bootstrap5 -n message
[Item #1] message.html, Success!
```

### 复制主题下所有文件

使用 `-a` 复制bootstrap5主题的所有模板文件。

```text
E:\projects\zinc> python .\manage.py starttpl bootstrap5 -a
about.html, Success!
base.html, Success!
detail.html, Success!
detail_frontend.html, Success!
home.html, Success!
items_grid.html, Success!
items_list.html, Success!
list.html, Success!
list_with_paginator.html, Success!
message.html, Success!
```

