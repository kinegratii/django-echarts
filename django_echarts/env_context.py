import os


def get_pyecharts_template_dir() -> str:
    import pyecharts
    base_dir = os.path.join(os.path.dirname(str(pyecharts.__file__)), 'render', 'templates')
    return base_dir


def get_django_echart_template_dir() -> str:
    return os.path.join(os.path.dirname(str(__file__)), 'templates')


def get_code_snippet_dir(*args: str) -> str:
    return os.path.join(os.path.dirname(str(__file__)), 'templates', 'snippets', *args)
