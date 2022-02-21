# 命令行工具

django-echarts 提供了一个包含若干个命令的 CLI 工具，这些命令都是标准的 Django 管理命令，均定义在 `django_echarts.management.commands` 包下。

你可以使用以下命令查看帮助信息。

```shell
python manage.py <command> -h
```

## info - 下载器-查看

```text
E:\projects\django-echarts\example>python manage.py info -h
usage: manage.py info [-h] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO] [--version] [-v {0,1,2,3}]
                      [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color]
                      [--skip-checks]

Show one or some dependency files.

optional arguments:
  -h, --help            show this help message and exit
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.
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

## download - 下载器-下载

```text
E:\projects\django-echarts\example>python manage.py download -h
usage: manage.py download [-h] [--dep DEP [DEP ...]] [--theme THEME] [--repo REPO] [--override] [--version]
                          [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color]
                          [--force-color] [--skip-checks]

Download one or some dependency files from remote CDN to project staticfile dirs.

optional arguments:
  -h, --help            show this help message and exit
  --dep DEP [DEP ...], -d DEP [DEP ...]
                        The name of dependency files.
  --theme THEME, -t THEME
                        The name of theme.
  --repo REPO, -r REPO  The name of dependency repo.
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

