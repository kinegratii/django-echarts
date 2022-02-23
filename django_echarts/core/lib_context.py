"""
The functions for accessing information of pyecharts & django-echarts library installed in python site-packages.
"""

import os

_pro_dir = os.path.dirname(os.path.dirname(str(__file__)))


def get_pyecharts_template_dir() -> str:
    import pyecharts
    base_dir = os.path.join(os.path.dirname(str(pyecharts.__file__)), 'render', 'templates')
    return base_dir


def get_django_echarts_template_dir(*args: str) -> str:
    return os.path.join(_pro_dir, 'templates', *args)


def get_code_snippet_dir(*args: str) -> str:
    return os.path.join(_pro_dir, 'templates', 'snippets', *args)
