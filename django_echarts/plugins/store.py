# coding=utf8
from dataclasses import dataclass, is_dataclass, field
import warnings
from typing import Dict

from django_echarts.plugins.hosts import LibHostStore, MapHostStore, JsUtils


@dataclass
class DJEOpts:
    echarts_version: str = '4.8.0'
    renderer: str = 'svg'
    lib_repo: str = 'pyecharts'
    map_repo: str = 'pyecharts'
    local_repo: str = ''
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
        _u('local_host', 'local_repo')

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
        elif is_dataclass(echarts_settings):
            self._opts = echarts_settings()
        else:
            self._opts = DJEOpts()

        # self._settings = {**DEFAULT_SETTINGS, **echarts_settings}

        self.lib_host_store = None
        self.map_host_store = None

        # self._check()
        self._setup()

    def _check(self):
        local_host = self._settings.get('local_host')
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

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        # TODO All entry point
        # Find in user settings first.
        link = self._opts.file2map.get(js_name)
        if link:
            return link
        if JsUtils.is_lib_js(js_name):
            hs = self.lib_host_store
            if not js_host:
                js_host = self._opts.lib_repo
        else:
            hs = self.map_host_store
            if not js_host:
                js_host = self._opts.map_repo
        if js_name == 'echarts' and js_host == 'pyecharts':
            js_name = 'echarts.min'
        return hs.generate_js_link(js_name=js_name, js_host=js_host)

    def generate_lib_js_link(self, js_name, js_host=None, **kwargs):
        return self.lib_host_store.generate_js_link(js_name=js_name, js_host=js_host)

    def generate_map_js_link(self, js_name, js_host=None, **kwargs):
        return self.map_host_store.generate_js_link(js_name=js_name, js_host=js_host)

    def generate_local_url(self, js_name):
        """
        Generate the local url for a js file.
        :param js_name:
        :return:
        """
        # TODO Refactor
        host = self._settings['local_host'].format(**self._host_context).rstrip('/')
        return '{}/{}.js'.format(host, js_name)

    @property
    def settings(self):
        return self._settings

    def get(self, key, default=None):
        return getattr(self._opts, key, default)
