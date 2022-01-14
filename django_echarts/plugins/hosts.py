# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""
from collections import defaultdict
from typing import Optional, Dict, Union

BUILTIN_LIB_REPOS = {
    'pyecharts': 'https://assets.pyecharts.org/assets/',
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}',
    'echarts': 'http://echarts.baidu.com/dist'
}

BUILTIN_MAP_REPOS = {
    'pyecharts': 'https://assets.pyecharts.org/assets/maps/',
    'china-provinces': 'https://echarts-maps.github.io/echarts-china-provinces-js/',
    'china-cities': 'https://echarts-maps.github.io/echarts-china-cities-js/',
    'united-kingdom': 'https://echarts-maps.github.io/echarts-united-kingdom-js'
}
CUSTOM_FILE_MAP = {
    'pyecharts': {'echarts': '@echarts.min'}
}


class JsUtils:
    ECHARTS_LIB_NAMES = [
        'echarts.common', 'echarts.common.min',
        'echarts', 'echarts.min',
        'echarts.simple', 'echarts.simple.min',
        'extension/bmap', 'extension/bmap.min',
        'extension/dataTool', 'extension/dataTool.min'
    ]

    @staticmethod
    def is_lib_js(js_name):
        return js_name in JsUtils.ECHARTS_LIB_NAMES


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


class DependencyManager:
    def __init__(self, *, context: dict = None, lib_repo=None, map_repo=None):
        self._context = context or {}
        self._repo_dic = {
            'lib': {},
            'map': {}
        }

        self._repo_f2map = defaultdict(dict)
        self._global_f2map = {}  # type:
        self._selected_lib_repo = lib_repo
        self._selected_map_repo = map_repo

    def add_repo(self, repo_name: str, repo_url: str, catalog: str):
        self._repo_dic[catalog].update({repo_name: repo_url})

    def add_f2item(self, value: Union[str, Dict], dep_name: Optional[str] = None, repo_name: Optional[str] = None):
        if repo_name:
            assert isinstance(value, dict)
            self._repo_f2map[repo_name].update(value)
        else:
            assert isinstance(value, str)
            self._global_f2map[dep_name] = value

    def resolve_url(self, dep_name: str, repo_name: str = None) -> str:
        value = self._global_f2map.get(dep_name)
        if value:
            vdep, vurl = _parse_val(value)
            if vurl:
                return vurl
            dep_name = vdep
        if JsUtils.is_lib_js(dep_name):
            catalog = 'lib'
            repo_name = repo_name or self._selected_lib_repo
        else:
            catalog = 'map'
            repo_name = repo_name or self._selected_map_repo
        value = self._repo_f2map.get(repo_name, {}).get(dep_name, '')
        if value:
            vdep, vurl = _parse_val(value)
            if vurl:
                return vurl
            dep_name = vdep
        filename = d2f(dep_name)
        url_fmt = self._repo_dic[catalog].get(repo_name).rstrip('/')
        return '{}/{}'.format(url_fmt.format(**self._context), filename)

    def resolve_available_url(self, dep_name: str, repo_name: str = None):
        """查找可下载的远程url"""
        pass

    @classmethod
    def create_default(cls, context: dict, lib_repo: str, map_repo: str) -> 'DependencyManager':
        manager = cls(context=context, lib_repo=lib_repo, map_repo=map_repo)
        for name, url in BUILTIN_LIB_REPOS.items():
            manager.add_repo(name, url, catalog='lib')
        for name, url in BUILTIN_MAP_REPOS.items():
            manager.add_repo(name, url, catalog='map')
        for k, v in CUSTOM_FILE_MAP.items():
            if isinstance(v, dict):
                manager.add_f2item(repo_name=k, value=v)
            else:
                manager.add_f2item(dep_name=k, value=v)

        return manager


class HostStore:
    HOST_DICT = {}

    def __init__(self, *, context=None, default_host=None):
        self._context = context or {}
        self._host_dict = {} or self.HOST_DICT
        self._default_host = self._ensure_host_url(default_host)

    def add_host(self, host_url, host_name=None):
        host_url = self._ensure_host_url(host_url)
        host_name = host_name or host_url
        self._host_dict.update({host_name: host_url})

    def generate_js_link(self, js_name, js_host=None):
        custom_f2m = CUSTOM_FILE_MAP.get(js_host, {})
        val = custom_f2m.get(js_name)
        if val:
            if val.startswith('@'):
                js_name = val[1:]
            else:
                return val
        if js_host:
            host_url = self._ensure_host_url(js_host)
        else:
            host_url = self._default_host
        if host_url is None:
            raise ValueError('No host is specified.')
        filename = d2f(js_name)
        return f'{host_url}/{filename}'

    def _ensure_host_url(self, name_or_url):
        host_url = self._host_dict.get(name_or_url, name_or_url)
        return host_url.format(**self._context).rstrip('/')

    @staticmethod
    def from_hosts(context, hosts, default_host):
        hs = HostStore(context=context, default_host=default_host)
        for k, v in hosts.items():
            hs.add_host(v, k)
        return hs


class LibHostStore(HostStore):
    HOST_DICT = BUILTIN_LIB_REPOS


class MapHostStore(HostStore):
    HOST_DICT = BUILTIN_MAP_REPOS
