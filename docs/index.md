# Django-Echarts Document

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
    'js_host':'cdnjs'
}
```

Or you my not define the variable and use all default values.

Read *API-Setings* charter to see more details. 
