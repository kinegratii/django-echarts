# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""
from typing import Tuple, List

from pyecharts.datasets import FILENAMES, EXTRA
from pyecharts._version import __version__ as pyecharts_version
from django_echarts.utils.burl import BUrl
from .localfiles import LocalFilesMixin, DownloaderResource

__all__ = ['DependencyManager']

# The repo contains all dependencies
_BUILTIN_REPOS_ = {
    'pyecharts': 'https://assets.pyecharts.org/assets/',
    'pycharts-v5': 'https://assets.pyecharts.org/assets/v5',
    'local': '/static/assets/'
}


class PyechartsDMS:
    VERSION2REPO = {
        '1.9': {'dms_repo': 'pyecharts', 'echarts_version': '4.8.0'},
        '2.0': {'dms_repo': 'pycharts-v5', 'echarts_version': '5.4.1'}
    }

    @staticmethod
    def get_pyecharts__primary_version():
        return pyecharts_version[:3]

    @staticmethod
    def get_pycharts_repo(version_pre: str):
        return PyechartsDMS.VERSION2REPO.get(version_pre)


# Use #REPO in custom d2u
_OTHER_REPOS_ = {
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcdn.net/ajax/libs/echarts/{echarts_version}',
    'china-provinces': 'https://echarts-maps.github.io/echarts-china-provinces-js/',
    'china-cities': 'https://echarts-maps.github.io/echarts-china-cities-js/',
    'united-kingdom': 'https://echarts-maps.github.io/echarts-united-kingdom-js'
}

_PYECHARTS_VERSIONS_ = {
    '1.9': {'dms_repo': 'pyecharts', 'echarts_version': '4.8.0'},
    '2.0': {'dms_repo': 'pycharts-v5', 'echarts_version': '5.4.1'}
}


def d2f(dep_name: str):
    if dep_name.endswith('.css') or dep_name.endswith('.js'):
        return dep_name
    else:
        return f'{dep_name}.js'


class DependencyManager(LocalFilesMixin):
    def __init__(self, *, context: dict = None, repo_name: str = None):
        self._context = context or {}
        self._repo_dic = {}
        self._custom_dep2url = {}  # depname=> url
        self._cur_repo_name = repo_name
        self._baidu_map_ak = self._context.get('baidu_map_ak')

    def add_repo(self, repo_name: str, repo_url: str):
        self._repo_dic[repo_name] = repo_url

    def load_from_dep2url_dict(self, d2u_dic: dict):
        """Parse user custom dep_url dict
        Update 0.6.0: support #repo key-value."""
        for k, v in d2u_dic.items():
            if k.startswith('#') and isinstance(v, (list, tuple)):
                for _v in v:
                    self._custom_dep2url[_v] = k
            else:
                self._custom_dep2url[k] = v

    def _resolve_dep(self, dep_name: str, repo_name: str = None) -> Tuple:
        if dep_name in self._custom_dep2url:
            value = self._custom_dep2url[dep_name]
            if value.startswith('#'):
                repo_name = value[1:]
            else:
                value = value.format(**self._context)
                return value, d2f(dep_name)
        repo_name = repo_name or self._cur_repo_name
        if repo_name not in self._repo_dic:
            raise ValueError(f'Unknown dms repo: {repo_name}. Choices are:{",".join(self._repo_dic.keys())}')

        use_url, new_dep_name = self._pyecharts_resolve_dep_name(dep_name)
        if use_url:
            return new_dep_name, None
        filename = d2f(new_dep_name)
        url_fmt = self._repo_dic.get(repo_name).rstrip('/')
        url = '{}/{}'.format(url_fmt.format(**self._context), filename)
        return url, filename

    def resolve_url(self, dep_name: str, repo_name: str = None) -> str:
        url, _ = self._resolve_dep(dep_name, repo_name)
        return url

    def get_download_resources(self, dep_names: List[str], repo_name: str = None) -> List[DownloaderResource]:
        resources = []
        for dep_name in dep_names:
            url, filename = self._resolve_dep(dep_name, repo_name)
            local_ref_url, local_path = self.localize_url(filename)
            resources.append(
                DownloaderResource(url, local_ref_url, local_path, label=dep_name, catalog='Dependency')
            )
        return resources

    def _pyecharts_resolve_dep_name(self, dep_name: str) -> Tuple[bool, str]:
        if all([
            self._baidu_map_ak,
            dep_name.startswith('https://api.map.baidu.com/') or dep_name.startswith('http://api.map.baidu.com/'),
            'ak=' in dep_name
        ]):
            # Replace baidu map ak with global settings.
            return True, BUrl(dep_name).replace('ak', self._baidu_map_ak).url
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

    @classmethod
    def create_default(cls, context: dict = None, repo_name: str = None):
        manager = cls(context=context, repo_name=repo_name)
        for k, v in _BUILTIN_REPOS_.items():
            manager.add_repo(k, v)
        return manager
