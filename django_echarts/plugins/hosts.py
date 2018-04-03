# coding=utf8
"""
A Implement that you can use host name instead of its url.
"""

ECHARTS_LIB_HOSTS = {
    'pyecharts': 'https://pyecharts.github.io/jupyter-echarts/echarts',
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}',
    'echarts': 'http://echarts.baidu.com/dist'
}

ECHARTS_MAP_HOSTS = {
    'echarts': 'http://echarts.baidu.com/asset/map/js',
    'china-provinces': 'https://echarts-maps.github.io/echarts-china-provinces-js/',
    'china-cities': 'https://echarts-maps.github.io/echarts-china-cities-js/',
    'united-kingdom': 'https://echarts-maps.github.io/echarts-united-kingdom-js'
}


class JsUtils(object):
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


class HostStore(object):
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
        if js_host:
            host_url = self._ensure_host_url(js_host)
        else:
            host_url = self._default_host
        if host_url is None:
            raise ValueError('No host is specified.')
        return '{}/{}.js'.format(host_url, js_name)

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
    HOST_DICT = ECHARTS_LIB_HOSTS


class MapHostStore(HostStore):
    HOST_DICT = ECHARTS_MAP_HOSTS
