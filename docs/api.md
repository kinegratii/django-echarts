# API

The API is under the developement, and any API has been NOT STABLE yet.

## App Settings

The default value are listed as the following code fragment.

```python
{
    'echarts_version':'3.7.0',
    'js_host':'bootcdn'
}
```

### js_host

The repository which project provides javascript static files.The following values are available:

- A CDN name: valid choices are `cdnjs` / `npmcdn` /` bootcdn` / `pyecharts`.
- A format string representing the host url,which supports the following CASE-SENSITIVE fields.
  - STATIC_URL: the value of `settings.STATIC_URL`
  - echarts_version: the version of echarts.

For example,if use  local static file`/static/echarts/echarts.min.js`,follow thesse steps:

Step 1:Config the settings module

```python
STATIC_URL = '/static/'
DJANGO_ECHARTS = {
    'js_host':'{STATIC_URL}echarts'
}
```

Step 2:Use template tag grammar `{% echarts_scripts line %}` will produce these code in the template html.

```html
<script src="/static/echarts/echarts.min.js"></script>
```

If you want to switch to CDN  when deploying to production environment,just set *js_host* to a CDN name(e.g bootcdn).

```html
<script src="https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js"></script>
```

### echarts_version

The version string of echarts which you are using. e.g `3.7.0`.It is used for the most CDN hosts.

## Global Settings Object

You can access these settings using  the module variable  `django_echarts.utils.DJANGO_ECHARTS_SETTING`.It is a dict-like object. You can also access using   `DJANGO_ECHARTS_SETTING['foo']` or `DJANGO_ECHARTS_SETTING.foo` .

### SettingsStore

`django_echarts.utils.SettingsStore`

A public settings class for access in the project.

## Template Tags

### echarts_options

`django_echarts.templatetags.echarts.echarts_options(echarts)`

Render javascript template for a Echarts objects.

## echarts_js

> This tag is deprecated.

`django_echarts.templatetags.echarts.echarts_js(echarts)`

Render javascript  script nodes for a echarts's js dependencies .

### echarts_scripts

`django_echarts.templatetags.echarts.echarts_scripts(*args)`

Render javascript script nodes for echarts,custom name.It is a enhance version of `echarts_js`.



## Plugins

*django-echarts* provides some plugins to enhance features.s 

### HostStore

`django_echarts.plugins.host.HostStore(name_or_host, context=None)`

A javascript host manager.

## Data Builder Tools

These method will be useful when you add data to `Base` instance from other formats. 

### Cast

`pyecharts.base.Base.cast(seq)`

A static method to Convert the sequence with the dictionary and tuple type into k_lst, v_lst.

### Pluck

`pluck.pluck(iterable, *keys, **kwargs)`

Pick fields from a iterable.
