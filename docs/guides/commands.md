# 命令行工具

django-echarts 提供了一个包含若干个命令的 CLI 工具，这些命令都是标准的 Django 管理命令，均定义在 `django_echarts.management.commands` 包下。

你可以使用以下命令查看帮助信息。

```shell
python manage.py <command> -h
```

## download

```shell
python manage.py download -h
```

## listdeps

```shell
E:\projects\django-echarts\example>python manage.py listdeps -h
usage: manage.py deps [-h] [--repo_name REPO_NAME] [--fake] [--version] [-v {0,1,2,3}] [--settings SETTINGS]
                      [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color] [--skip-checks]
                      dep_name [dep_name ...]

The manage command for dependency.

positional arguments:
  dep_name              The name of dependency files.

optional arguments:
  -h, --help            show this help message and exit
  --repo_name REPO_NAME
                        The name of a repository.
  --fake, -f            Just print download meta info and do not download..
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided,
                        the DJANGO_SETTINGS_MODULE environment variable will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.
```

### 查看所有仓库

```
E:\projects\django-echarts\example>python manage.py listdep
+---------+-----------------+------------------------------------------------------------+
| Catalog |     RepoName    |                          RepoUrl                           |
+---------+-----------------+------------------------------------------------------------+
|   lib   |    pyecharts    |            https://assets.pyecharts.org/assets/            |
|   lib   |      cdnjs      |    https://cdnjs.cloudflare.com/ajax/libs/echarts/4.8.0    |
|   lib   |      npmcdn     |            https://unpkg.com/echarts@4.8.0/dist            |
|   lib   |     bootcdn     |           https://cdn.bootcss.com/echarts/4.8.0            |
|   map   |    pyecharts    |         https://assets.pyecharts.org/assets/maps/          |
|   map   | china-provinces | https://echarts-maps.github.io/echarts-china-provinces-js/ |
|   map   |   china-cities  |  https://echarts-maps.github.io/echarts-china-cities-js/   |
|   map   |  united-kingdom |  https://echarts-maps.github.io/echarts-united-kingdom-js  |
+---------+-----------------+------------------------------------------------------------+
```

### 查看某个依赖项


```
E:\projects\django-echarts\example>python manage.py listdep --dep_name echarts --status
DependencyName:echarts
Catalog:lib
+-------+-----------+-----------------------------------------------------------------+---------+
| Order |  RepoName |                              DepUrl                             |  Status |
+-------+-----------+-----------------------------------------------------------------+---------+
|   1   | pyecharts |        https://assets.pyecharts.org/assets/echarts.min.js       | Success |
|   2   |   cdnjs   | https://cdnjs.cloudflare.com/ajax/libs/echarts/4.8.0/echarts.js | Success |
|   3   |   npmcdn  |         https://unpkg.com/echarts@4.8.0/dist/echarts.js         | Success |
|   4   |  bootcdn  |         https://cdn.bootcss.com/echarts/4.8.0/echarts.js        | Success |
+-------+-----------+-----------------------------------------------------------------+---------+
```

## startsite

创建 初始化site的代码片段。

```shell
E:\projects\django-echarts\example>python manage.py startsite -h
usage: manage.py startsite [-h] [--site-title SITE_TITLE] [--start-year START_YEAR] [--powered-by POWERED_BY]
                           [--override] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH]
                           [--traceback] [--no-color] [--force-color] [--skip-checks]
                           output

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
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided,
                        the DJANGO_SETTINGS_MODULE environment variable will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.
```

