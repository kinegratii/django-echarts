# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""
import warnings
from collections import defaultdict, namedtuple
from dataclasses import dataclass, is_dataclass, field
from typing import Optional, Dict, Union, List, Callable

from pyecharts.datasets import FILENAMES as MAP_FILENAME_DICT

__all__ = ['DependencyManager', 'DJEOpts', 'SettingsStore']

BUILTIN_LIB_REPOS = {
    'pyecharts': 'https://assets.pyecharts.org/assets/',
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcdn.net/ajax/libs/echarts/{echarts_version}',
}

BUILTIN_MAP_REPOS = {
    'pyecharts': 'https://assets.pyecharts.org/assets/',
    'china-provinces': 'https://echarts-maps.github.io/echarts-china-provinces-js/',
    'china-cities': 'https://echarts-maps.github.io/echarts-china-cities-js/',
    'united-kingdom': 'https://echarts-maps.github.io/echarts-united-kingdom-js'
}


def _resolve_pyecharts_map_dep(dep_name: str):
    if dep_name in MAP_FILENAME_DICT:
        return MAP_FILENAME_DICT[dep_name][0]
    else:
        return dep_name


_CUSTOM_D2U_MAP = {
    '#pyecharts': {'echarts': '@echarts.min', 'echarts-gl': '@echarts-gl.min'},
    'echarts-gl': 'https://assets.pyecharts.org/assets/echarts-gl.min.js'
}

ECHARTS_LIB_NAMES = [
    'echarts.common', 'echarts.common.min',
    'echarts', 'echarts.min', 'echarts-gl', 'echarts-gl.min',
    'echarts.simple', 'echarts.simple.min',
    'extension/bmap', 'extension/bmap.min',
    'extension/dataTool', 'extension/dataTool.min'
]


def _is_lib_dep(dep_name):
    return dep_name in ECHARTS_LIB_NAMES


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


RemoteResource = namedtuple('RemoteResource', 'catalog repo_name url')


class DependencyManager:
    def __init__(self, *, context: dict = None, lib_repo=None, map_repo=None):
        self._context = context or {}
        self._repo_dic = {
            'lib': {},
            'map': {}
        }

        self._repo_f2map = defaultdict(dict)
        self._global_f2map = {}
        self._selected_lib_repo = lib_repo
        self._selected_map_repo = map_repo
        self._dep_call_dict = {}

    def add_repo(self, repo_name: str, repo_url: str, catalog: str):
        self._repo_dic[catalog].update({repo_name: repo_url})

    def add_f2item(self, value: Union[str, Dict], dep_name: Optional[str] = None, repo_name: Optional[str] = None):
        if repo_name:
            assert isinstance(value, dict)
            self._repo_f2map[repo_name].update(value)
        else:
            # global
            assert isinstance(value, str)
            self._global_f2map[dep_name] = value

    def add_dep_call(self, repo_name: str, call: Callable):
        self._dep_call_dict[repo_name] = call

    def load_from_d2u_dict(self, d2u_dic: dict):
        for k, v in d2u_dic.items():  # TODO sorted
            if k.startswith('#'):
                if isinstance(v, dict):
                    self._repo_f2map[k[1:]].update(v)
                if isinstance(v, str):
                    # new repo
                    if k[-4:] == '.lib' or k[-4:] == '.map':
                        repo_name = k[1:-4]
                    else:
                        repo_name = k[1:]
                    if k[-4:] != '.map':
                        self._repo_dic['lib'].update({repo_name: v})
                    if k[-4:] != '.lib':
                        self._repo_dic['map'].update({repo_name: v})
            elif isinstance(v, str):
                self._global_f2map[k] = v

    def resolve_url(self, dep_name: str, repo_name: str = None) -> str:
        value = self._global_f2map.get(dep_name)
        if value:
            vdep, vurl = _parse_val(value)
            if vurl:
                return _format_static_url(vurl, self._context)
            dep_name = vdep
        if _is_lib_dep(dep_name):
            catalog = 'lib'
            repo_name = repo_name or self._selected_lib_repo
        else:
            catalog = 'map'
            repo_name = repo_name or self._selected_map_repo
        value = self._repo_f2map.get(repo_name, {}).get(dep_name, '')
        if value:
            vdep, vurl = _parse_val(value)
            if vurl:
                return _format_static_url(vurl, self._context)
            dep_name = vdep
        else:
            func_key = f'{repo_name}.{catalog}'
            if func_key in self._dep_call_dict:
                dep_name = self._dep_call_dict[func_key](dep_name)
        filename = d2f(dep_name)
        url_fmt = self._repo_dic[catalog].get(repo_name).rstrip('/')
        return '{}/{}'.format(url_fmt.format(**self._context), filename)

    def resolve_all_urls(self, dep_name: str) -> List[RemoteResource]:
        """列出所有Repo中某个dep_name的远程url."""

        all_urls = []
        # Global Resolve
        if _is_lib_dep(dep_name):
            catalog = 'lib'
        else:
            catalog = 'map'
        value = self._global_f2map.get(dep_name)
        if value:
            vdep, vurl = _parse_val(value)
            if vurl:
                all_urls.append(RemoteResource(catalog=catalog, repo_name='[Custom]', url=vurl))
            dep_name = vdep
        if _is_lib_dep(dep_name):
            catalog = 'lib'
        else:
            catalog = 'map'

        for _rname, _rurl in self._repo_dic[catalog].items():
            name = dep_name
            value = self._repo_f2map.get(_rname, {}).get(dep_name, '')
            if value:
                vdep, vurl = _parse_val(value)
                if vurl:
                    all_urls.append(all_urls.append(RemoteResource(catalog=catalog, repo_name=_rname, url=vurl)))
                    continue
                name = vdep
            filename = d2f(name)
            url_fmt = _rurl.rstrip('/')
            url = '{}/{}'.format(url_fmt.format(**self._context), filename)
            all_urls.append(RemoteResource(catalog=catalog, repo_name=_rname, url=url))
        return all_urls

    def iter_repos(self):
        for catalog, repos in self._repo_dic.items():
            for repo_name, repo_url in repos.items():
                yield catalog, repo_name, repo_url.format(**self._context)

    @classmethod
    def create_default(cls, context: dict, lib_repo: str = None, map_repo: str = None) -> 'DependencyManager':
        manager = cls(context=context, lib_repo=lib_repo, map_repo=map_repo)
        for name, url in BUILTIN_LIB_REPOS.items():
            manager.add_repo(name, url, catalog='lib')
        for name, url in BUILTIN_MAP_REPOS.items():
            manager.add_repo(name, url, catalog='map')
        manager.load_from_d2u_dict(_CUSTOM_D2U_MAP)
        manager.add_dep_call('pyecharts.map', _resolve_pyecharts_map_dep)
        return manager


@dataclass
class DJEOpts:
    echarts_version: str = '4.8.0'
    renderer: str = 'svg'
    lib_repo: str = 'pyecharts'
    map_repo: str = 'pyecharts'
    local_dir: str = ''
    lib_local_dir: str = ''
    map_local_dir: str = ''
    file2map: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self.map_local_dir = self.map_local_dir or self.local_dir
        self.lib_local_dir = self.lib_local_dir or self.local_dir

    @staticmethod
    def upgrade_dict(vals: dict):
        def _u(_old, _new):
            val = vals.pop(_old, None)
            if val:
                warnings.warn(f'Option {_old} is deprecated. Use {_new} instead.', DeprecationWarning)
                if _new not in vals:
                    vals[_new] = val

        _u('lib_js_host', 'lib_repo')
        _u('map_js_host', 'map_repo')
        _u('local_host', 'local_dir')

        return vals


# SettingsStore -> DependencyManage -> DJEOpts
class SettingsStore:
    def __init__(self, *, echarts_settings=None, extra_settings=None, **kwargs):
        # Pre check settings

        self._extra_settings = extra_settings or {}

        if isinstance(echarts_settings, dict):
            self._opts = DJEOpts(**DJEOpts.upgrade_dict(echarts_settings))
        elif isinstance(echarts_settings, DJEOpts):
            self._opts = echarts_settings
        elif is_dataclass(echarts_settings):
            self._opts = echarts_settings()
        else:
            self._opts = DJEOpts()

        self._context = {'echarts_version': self._opts.echarts_version}
        if 'STATIC_URL' in self._extra_settings:
            self._context.update({'STATIC_URL': self._extra_settings['STATIC_URL']})
        self._manager = DependencyManager.create_default(
            context=self._context,
            lib_repo=self._opts.lib_repo,
            map_repo=self._opts.map_repo
        )
        self._manager.load_from_d2u_dict(self._opts.file2map)

        # self._setup()

    def _check(self):
        local_host = self._opts.local_dir
        static_url = self._extra_settings.get('STATIC_URL')
        if local_host:
            if static_url:
                if not local_host.startswith('{STATIC_URL}') and not local_host.startswith(static_url):
                    raise ValueError('The local_host must start with the value of "settings.STATIC_URL"')
            else:
                raise ValueError("The local_host item requires a no-empty settings.STATIC_URL.")

    # #### Public API: Generate js link using current configure ########

    @property
    def dependency_manager(self) -> DependencyManager:
        return self._manager

    def resolve_url(self, dep_name: str, repo_name: Optional[str] = None):
        return self._manager.resolve_url(dep_name, repo_name)

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        warnings.warn('The method SettingsStore.generate_js_link is deprecated, use SettingsStore.resolve_url instead.',
                      DeprecationWarning, stacklevel=2)
        return self._manager.resolve_url(dep_name=js_name, repo_name=js_host)

    def get_local_dir(self, dep_name):
        if _is_lib_dep(dep_name):
            return self._opts.lib_local_dir
        else:
            return self._opts.map_local_dir

    def generate_local_url(self, js_name):
        """
        Generate the local url for a js file.
        """
        # TODO Refactor
        dir_s = self.get_local_dir(js_name)
        host = dir_s.format(**self._context).rstrip('/')
        return '{}/{}.js'.format(host, js_name)

    def get(self, key, default=None):
        return getattr(self._opts, key, default)
