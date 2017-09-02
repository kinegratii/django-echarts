# Django-Echarts Document

> The API is under the developement, and any API has been NOT STABLE yet.

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

## API - Settings

All settings should define in a variable named `DJANGO_ECHARTS`.The default value are listed as the following code fragment.

```python
{
    'echarts_version':'3.7.0',
    'js_host':'localhost'
}
```

You can access these settings using  the module variable  `django_echarts.utils.DJANGO_ECHARTS_SETTING`.It is a dict-like object. You can also access using `DJANGO_ECHARTS_SETTING.foo` .

### js_host

The repository which project provides javascript static files.The following values are available:

- `'localhost'` :  Use `settings.STATIC_URL`.
- `pyecharts.constants.DEFAULT_HOST` : Use pyecharts javascript library.
- Any valid CDN url. e.g. `https://cdn.bootcss.com/echarts/3.7.0`

## API - Template Tags

### echarts_options

`django_echarts.templatetags.echarts.echarts_options(echarts)`

Render javascript template for a Echarts objects.

## echarts_js

`django_echarts.templatetags.echarts.echarts_js(echarts)`

Render script nodes for javascript dependencies of a echarts.