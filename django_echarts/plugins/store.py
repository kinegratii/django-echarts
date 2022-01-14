# coding=utf8
import warnings
from dataclasses import dataclass, is_dataclass, field
from typing import Dict, Optional

from django_echarts.plugins.hosts import DependencyManager
from django_echarts.plugins.hosts import LibHostStore, MapHostStore


@dataclass
class DJEOpts:
    echarts_version: str = '4.8.0'
    renderer: str = 'svg'
    lib_repo: str = 'pyecharts'
    map_repo: str = 'pyecharts'
    local_dir: str = ''
    file2map: Dict[str, str] = field(default_factory=dict)

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


class SettingsStore:
    def __init__(self, *, echarts_settings=None, extra_settings=None, **kwargs):
        # Pre check settings

        self._extra_settings = extra_settings or {}
        # if self._extra_settings.get('lib_js_host') == 'local_host':
        #     self._extra_settings['lib_js_host'] = echarts_settings['local_host']
        # if self._extra_settings.get('map_js_host') == 'local_host':
        #     self._extra_settings['map_js_host'] = echarts_settings['local_host']

        # Merge echarts settings
        if isinstance(echarts_settings, dict):
            self._opts = DJEOpts(**DJEOpts.upgrade_dict(echarts_settings))
        elif isinstance(echarts_settings, DJEOpts):
            self._opts = echarts_settings
        elif is_dataclass(echarts_settings):
            self._opts = echarts_settings()
        else:
            self._opts = DJEOpts()

        self._manager = DependencyManager.create_default(
            context={'echarts_version': self._opts.echarts_version},
            lib_repo=self._opts.lib_repo,
            map_repo=self._opts.map_repo
        )

        # self._settings = {**DEFAULT_SETTINGS, **echarts_settings}

        self.lib_host_store = None
        self.map_host_store = None

        # self._check()
        self._setup()

    def _check(self):
        local_host = self._opts.local_dir
        static_url = self._extra_settings.get('STATIC_URL')
        if local_host:
            if static_url:
                if not local_host.startswith('{STATIC_URL}') and not local_host.startswith(static_url):
                    raise ValueError('The local_host must start with the value of "settings.STATIC_URL"')
            else:
                raise ValueError("The local_host item requires a no-empty settings.STATIC_URL.")

    def _setup(self):
        self._host_context = {
            'echarts_version': self._opts.echarts_version
        }
        if 'STATIC_URL' in self._extra_settings:
            self._host_context.update({'STATIC_URL': self._extra_settings['STATIC_URL']})
        self.lib_host_store = LibHostStore(
            context=self._host_context,
            default_host=self._opts.lib_repo
        )
        self.map_host_store = MapHostStore(
            context=self._host_context,
            default_host=self._opts.map_repo
        )

    # #### Public API: Generate js link using current configure ########

    def resolve_url(self, dep_name: str, repo_name: Optional[str] = None):
        return self._manager.resolve_url(dep_name, repo_name)

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        warnings.warn('The method SettingsStore.generate_js_link is deprecated, use SettingsStore.resolve_url instead.',
                      DeprecationWarning, stacklevel=2)
        return self._manager.resolve_url(dep_name=js_name, repo_name=js_host)

    def generate_local_url(self, js_name):
        """
        Generate the local url for a js file.
        """
        # TODO Refactor
        host = self._opts.local_dir.format(**self._host_context).rstrip('/')
        return '{}/{}.js'.format(host, js_name)

    def get(self, key, default=None):
        return getattr(self._opts, key, default)
