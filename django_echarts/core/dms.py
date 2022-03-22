# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""
from typing import Tuple

from pyecharts.datasets import FILENAMES, EXTRA

__all__ = ['DependencyManager']


def pyecharts_resolve_dep_name(dep_name: str) -> Tuple[bool, str]:
    if dep_name.startswith("https://") or dep_name.startswith('http://'):
        return True, dep_name
    if dep_name in FILENAMES:
        f, ext = FILENAMES[dep_name]
        return False, "{}.{}".format(f, ext)
    else:
        for url, files in EXTRA.items():
            if dep_name in files:
                f, ext = files[dep_name]
                return False, "{}.{}".format(f, ext)
        return False, '{}.js'.format(dep_name)


# The repo contains all dependencies
_BUILTIN_REPOS_ = {
    'pyecharts': 'https://assets.pyecharts.org/assets/',
    'local': '/static/assets/'
}
# Use #REPO in custom d2u
_OTHER_REPOS_ = {
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcdn.net/ajax/libs/echarts/{echarts_version}',
    'china-provinces': 'https://echarts-maps.github.io/echarts-china-provinces-js/',
    'china-cities': 'https://echarts-maps.github.io/echarts-china-cities-js/',
    'united-kingdom': 'https://echarts-maps.github.io/echarts-united-kingdom-js'
}

_CUSTOM_D2U_MAP = {
    'echarts': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/4.8.0/echarts.min.js',
    'echarts-gl': 'https://assets.pyecharts.org/assets/echarts-gl.min.js'
}


def d2f(dep_name: str):
    if dep_name.endswith('.css') or dep_name.endswith('.js'):
        return dep_name
    else:
        return f'{dep_name}.js'


def _parse_val(value: str):
    if value.startswith('@'):
        return value[1:], ''
    else:
        return '', value


def _format_static_url(url: str, context: dict) -> str:
    if '{STATIC_URL}' in url and 'STATIC_URL' not in context:
        raise ValueError(f'Can not parse {url} without STATIC_URL value.')
    return url.format(**context)


class DependencyManager:
    def __init__(self, *, context: dict = None, repo_name: str = None):
        self._context = context or {}
        self._repo_dic = {}
        self._custom_dep2url = {}  # depname=> url
        self._cur_repo_name = repo_name

    def add_repo(self, repo_name: str, repo_url: str):
        self._repo_dic[repo_name] = repo_url

    def load_from_dep2url_dict(self, d2u_dic: dict):
        self._custom_dep2url.update(d2u_dic)

    def _resolve_dep(self, dep_name: str, repo_name: str = None) -> Tuple:
        if dep_name in self._custom_dep2url:
            value = self._custom_dep2url[dep_name]
            if value.startswith('#'):
                repo_name = value[1:]
            else:
                return value, d2f(dep_name)
        repo_name = repo_name or self._cur_repo_name
        if repo_name not in self._repo_dic:
            raise ValueError(f'Unknown dms repo: {repo_name}. Choices are:{",".join(self._repo_dic.keys())}')

        use_url, new_dep_name = pyecharts_resolve_dep_name(dep_name)
        if use_url:
            return new_dep_name, None
        filename = d2f(new_dep_name)
        url_fmt = self._repo_dic.get(repo_name).rstrip('/')
        url = '{}/{}'.format(url_fmt.format(**self._context), filename)
        return url, filename

    def resolve_url(self, dep_name: str, repo_name: str = None) -> str:
        url, _ = self._resolve_dep(dep_name, repo_name)
        return url

    def iter_download_resources(self, dep_names: str, repo_name: str = None):
        for dep_name in dep_names:
            url, filename = self._resolve_dep(dep_name, repo_name)
            if filename:
                yield dep_name, url, filename

    @classmethod
    def create_default(cls, context: dict = None, repo_name: str = None):
        manager = cls(context=context, repo_name=repo_name)
        for k, v in _BUILTIN_REPOS_.items():
            manager.add_repo(k, v)
        return manager
