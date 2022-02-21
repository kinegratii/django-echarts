# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""
import warnings
from dataclasses import dataclass, is_dataclass, field
from typing import Optional, Dict, Union, Tuple

from pyecharts.datasets import FILENAMES, EXTRA

__all__ = ['DependencyManager', 'DJEOpts', 'SettingsStore']


def pyecharts_resolve_dep_name(dep_name):
    if dep_name.startswith("https://api.map.baidu.com"):
        return dep_name
    if dep_name in FILENAMES:
        f, ext = FILENAMES[dep_name]
        return "{}.{}".format(f, ext)
    else:
        for url, files in EXTRA.items():
            if dep_name in files:
                f, ext = files[dep_name]
                return "{}.{}".format(f, ext)
        return '{}.js'.format(dep_name)


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
        url_fmt = self._repo_dic.get(repo_name).rstrip('/')
        new_dep_name = pyecharts_resolve_dep_name(dep_name)
        filename = d2f(new_dep_name)

        url = '{}/{}'.format(url_fmt.format(**self._context), filename)
        return url, filename

    def resolve_url(self, dep_name: str, repo_name: str = None) -> str:
        url, _ = self._resolve_dep(dep_name, repo_name)
        return url

    def iter_download_resources(self, dep_names: str, repo_name: str = None):
        for dep_name in dep_names:
            url, filename = self._resolve_dep(dep_name, repo_name)
            yield dep_name, url, filename

    @classmethod
    def create_default(cls, context: dict = None, repo_name: str = None):
        manager = cls(context=context, repo_name=repo_name)
        for k, v in _BUILTIN_REPOS_.items():
            manager.add_repo(k, v)
        return manager


@dataclass
class DJEOpts:
    echarts_version: str = '4.8.0'
    renderer: str = 'svg'
    dms_repo: str = 'pyecharts'
    local_dir: str = ''
    dep2url: Dict[str, str] = field(default_factory=dict)
    enable_echarts_theme: bool = False

    echarts_theme: Union[bool, str] = False

    def get_echarts_theme(self, echarts_theme) -> str:
        if self.echarts_theme is False:
            return ''
        elif self.echarts_theme is True:
            return echarts_theme
        elif isinstance(self.echarts_theme, str):
            return self.echarts_theme
        else:
            return ''

    @staticmethod
    def upgrade_dict(vals: dict):
        def _u(_old, _new=None):
            val = vals.pop(_old, None)
            if val:
                warnings.warn(f'Option {_old} is deprecated. Use {_new} instead.', DeprecationWarning)
                if _new is not None and _new not in vals:
                    vals[_new] = val

        _u('map_js_host')
        _u('map_repo')
        _u('lib_js_host', 'dms_repo')
        _u('lib_repo', 'dms_repo')
        _u('local_host', 'local_dir')
        _u('file2map', 'dep2url')

        return vals


# SettingsStore -> DependencyManage -> DJEOpts
class SettingsStore:
    def __init__(self, *, echarts_settings=None, extra_settings=None, **kwargs):
        # Pre check settings

        self._extra_settings = extra_settings or {}

        if isinstance(echarts_settings, dict):
            new_opts = DJEOpts.upgrade_dict(echarts_settings)
            self._opts = DJEOpts(**new_opts)
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
            repo_name=self._opts.dms_repo
        )
        self._manager.load_from_dep2url_dict(self._opts.dep2url)

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
    def opts(self) -> DJEOpts:
        return self._opts

    @property
    def dependency_manager(self) -> DependencyManager:
        return self._manager

    def resolve_url(self, dep_name: str, repo_name: Optional[str] = None):
        return self._manager.resolve_url(dep_name, repo_name)

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        warnings.warn('The method SettingsStore.generate_js_link is deprecated, use SettingsStore.resolve_url instead.',
                      DeprecationWarning, stacklevel=2)
        return self._manager.resolve_url(dep_name=js_name, repo_name=js_host)

    def get(self, key, default=None):
        return getattr(self._opts, key, default)
