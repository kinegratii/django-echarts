# coding=utf8
"""A javascript host manager.
"""

from __future__ import unicode_literals

ECHARTS_LIB_HOSTS = {
    'pyecharts': 'https://chfw.github.io/jupyter-echarts/echarts',  # TODO Use pyecharts.constants.DEFAULT_HOST
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}'
}

ECHARTS_LIB_NAMES = [
    'echarts.common', 'echarts.common.min',
    'echarts', 'echarts.min',
    'echarts.simple', 'echarts.simple.min',
    'extension/bmap', 'extension/bmap.min',
    'extension/dataTool', 'extension/dataTool.min'
]

ECHARTS_MAP_HOSTS = {
    'pyecharts': 'https://chfw.github.io/jupyter-echarts/echarts',
    'echarts': 'http://echarts.baidu.com/asset/map/js'
}


def is_lib_or_map_js(js_name):
    return js_name in ECHARTS_LIB_NAMES


class HostMixin(object):
    def generate_js_link(self, js_name):
        raise NotImplemented()


class Host(HostMixin):
    HOST_LOOKUP = {}

    def __init__(self, name_or_host, context=None, host_lookup=None, **kwargs):
        context = context or {}
        host_lookup = host_lookup or self.HOST_LOOKUP
        host = host_lookup.get(name_or_host, name_or_host)
        try:
            self._host = host.format(**context).rstrip('/')
        except KeyError as e:
            self._host = None
            if 'STATIC_URL' in e.args:
                msg = 'You must define the value of STATIC_URL in your project settings module.'
            else:
                msg = 'The "{0}" value is not applied for the host.'.format(*e.args)
            raise KeyError(msg)

    @property
    def host_url(self):
        return self._host

    def generate_js_link(self, js_name, **kwargs):
        return '{0}/{1}.js'.format(self._host, js_name)


class HostStore(HostMixin):
    def __init__(self, context=None, echarts_lib_name_or_host=None, echarts_map_name_or_host=None, **kwargs):
        self._context = context or {}
        self._default_lib_name = echarts_lib_name_or_host
        self._default_map_name = echarts_map_name_or_host

        # Initialize
        self._url_dict = {('lib', k): v for k, v in ECHARTS_LIB_HOSTS.items()}
        self._url_dict.update({('map', k): v for k, v in ECHARTS_MAP_HOSTS.items()})
        self._host_dict = {
        }
        # add default
        self.install_default_hosts(self._default_lib_name, self._default_map_name)

    def add_new_host(self, catalog, host_url, host_name=None):
        host_name = host_name or host_url
        self._url_dict.update({(catalog, host_name): host_url})

    def install_default_hosts(self, lib_name_or_host, map_name_or_host):
        host_url = self._url_dict.get(('lib', lib_name_or_host), lib_name_or_host)
        host = Host(host_url, context=self._context)
        self._host_dict.update({('lib', lib_name_or_host): host})
        self._default_lib_name = lib_name_or_host

        host_url = self._url_dict.get(('map', map_name_or_host), map_name_or_host)
        host = Host(host_url, context=self._context)
        self._host_dict.update({('map', map_name_or_host): host})
        self._default_map_name = map_name_or_host

    def generate_js_link(self, js_name, js_host=None, only_lookup=False, **kwargs):
        if is_lib_or_map_js(js_name):
            lookup = 'lib', js_host or self._default_lib_name
        else:
            lookup = 'map', js_host or self._default_map_name
        host = self._host_dict.get(lookup)
        if host:
            pass
        else:
            if lookup in self._url_dict:
                host = Host(self._url_dict.get(lookup), context=self._context)
                self._host_dict[lookup] = host
            else:
                if only_lookup:
                    raise ValueError('No host found in onlyLookup mode.')
                else:
                    host = Host(js_host, self._context)
        return host.generate_js_link(js_name)


if __name__ == '__main__':
    import unittest


    class ATest(unittest.TestCase):
        def test_all(self):
            # Basic tests
            m_context = {
                'STATIC_URL': '/static/',
                'echarts_version': '3.7.0'
            }
            hs = HostStore(m_context, 'bootcdn', 'echarts')
            self.assertEqual(
                'https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js',
                hs.generate_js_link('echarts.min')
            )
            self.assertEqual(
                'http://echarts.baidu.com/asset/map/js/china.js',
                hs.generate_js_link('china')
            )
            # Use custom js_host
            self.assertEqual(
                'https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.0/echarts.min.js',
                hs.generate_js_link('echarts.min', js_host='cdnjs')
            )
            self.assertEqual(
                'https://chfw.github.io/jupyter-echarts/echarts/china.js',
                hs.generate_js_link('china', js_host='pyecharts')
            )
            # Add
            hs.add_new_host('map', 'https://amap.com/js', 'amap')
            self.assertEqual(
                'https://amap.com/js/fujian.js',
                hs.generate_js_link('fujian', 'amap')
            )


    unittest.main()
