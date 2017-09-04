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
    'js_host':'bootcdn'
}
```

You can access these settings using  the module variable  `django_echarts.utils.DJANGO_ECHARTS_SETTING`.It is a dict-like object. You can also access using   `DJANGO_ECHARTS_SETTING['foo']` or `DJANGO_ECHARTS_SETTING.foo` .

### js_host

The repository which project provides javascript static files.The following values are available:

- A CDN name: valid choices are `cdnjs` / `npmcdn` /` bootcdn` / `pyecharts`.
- A format string representing the host url:
  - STATIC_URL: the value of `settings.STATIC_URL`
  - echarts_version: the version of echarts.

### echarts_version

The version string of echarts which you are using. e.g `3.7.0`.It is used for the most CDN hosts.

## API - Template Tags

### echarts_options

`django_echarts.templatetags.echarts.echarts_options(echarts)`

Render javascript template for a Echarts objects.

## echarts_js

`django_echarts.templatetags.echarts.echarts_js(echarts)`

Render script nodes for javascript dependencies of a echarts.