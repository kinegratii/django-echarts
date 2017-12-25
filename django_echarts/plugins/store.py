# coding=utf8

from __future__ import unicode_literals

from django_echarts.plugins.hosts import LibHostStore, MapHostStore, JsUtils

DEFAULT_SETTINGS = {
    'echarts_version': '3.7.0',
    'lib_js_host': 'bootcdn',
    'map_js_host': 'echarts',
    'local_host': None
}


class SettingsStore(object):
    def __init__(self, echarts_settings=None, extra_settings=None, **kwargs):
        # Pre check settings
        self._settings = {k: v for k, v in DEFAULT_SETTINGS.items()}
        if echarts_settings:
            if echarts_settings['lib_js_host'] == 'local_host':
                echarts_settings['lib_js_host'] = echarts_settings['local_host']
            if echarts_settings['map_js_host'] == 'local_host':
                echarts_settings['map_js_host'] = echarts_settings['local_host']
            self._settings.update(echarts_settings)
        self._extra_settings = extra_settings or {}

        self.lib_host_store = None
        self.map_host_store = None

        self._check()
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
            'echarts_version': self._settings['echarts_version']
        }
        if 'STATIC_URL' in self._extra_settings:
            self._host_context.update({'STATIC_URL': self._extra_settings['STATIC_URL']})
        self.lib_host_store = LibHostStore(
            context=self._host_context,
            default_host=self._settings['lib_js_host']
        )
        self.map_host_store = MapHostStore(
            context=self._host_context,
            default_host=self._settings['map_js_host']
        )

    # #### Public API: Generate js link using current configure ########

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        if JsUtils.is_lib_js(js_name):
            hs = self.lib_host_store
        else:
            hs = self.map_host_store
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
        host = self._settings['local_host'].format(**self._host_context).rstrip('/')
        return '{}/{}.js'.format(host, js_name)

    @property
    def settings(self):
        return self._settings
