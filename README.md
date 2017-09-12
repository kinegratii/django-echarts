# django-echarts

![django-echarts version](https://img.shields.io/pypi/v/django-echarts.svg) ![python27](https://img.shields.io/badge/Python-2.7+-blue.svg) ![python35](https://img.shields.io/badge/Python-3.5+-blue.svg) ![django18](https://img.shields.io/badge/Django-1.8+-blue.svg)

A intergration for [Echarts](http://echarts.baidu.com/index.html) and [Django](https://www.djangoproject.com) based on [chenjiandongx/pyecharts](https://github.com/chenjiandongx/pyecharts) .

> This project is on the developement state, do not use in the production environment.

## Overview

django-echarts provides a set of shortcut tool for django intergration.These are:

- Simple data builder for echarts
- Renders using frontend ajax or templates
- Javascript host manager
- Some utils functions and classes

django-echarts covers the following django components.You should understand them before using django-echarts.

- View mixin
- template tags
- context processors
- Management commands

django-echarts works on Python2.7 / Python3.5+ and Django1.8+,and Python3 is **Strongly** recommended.

## Installation

You can install *django-echarts* from pip.

```
pip install django-echarts
```

or build from source code.

```
git clone https://github.com/kinegratii/django-echarts.git
cd django-echarts
python setup.py install
```

## Setup

1 Add django_charts app to your `INSTALL_APPS`.

```python
INSTALL_APPS = (
    # Your apps
    'django_echarts'
    # Your apps
)
```

2 Custom your settings with `DJANGO_ECHARTS` variable in the settings module.e.g

```python
DJANGO_ECHARTS = {
    'lib_js_host':'cdnjs'
}
```

Or you my not define the variable and use all default values.

Read *API* document to see more details.

## Example

The example project is under *example* directory.

```shell
cd example
python manage.py runserver 127.0.0.1:8000
```

Access the web url  http://127.0.0.1:8000 , the screencut is the following picture.

![Demo](images/demo1.gif)

## License

The project is under the MIT license, Issues & Pull requests are welcome.