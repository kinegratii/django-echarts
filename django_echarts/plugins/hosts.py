# coding=utf8

from __future__ import unicode_literals

ECHARTS_LIB_HOSTS = {
    'pyecharts': 'https://chfw.github.io/jupyter-echarts/echarts',  # Point to pyecharts.constants.DEFAULT_HOST
    'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
    'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
    'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}',
    'echarts': 'http://echarts.baidu.com/dist'
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


class HostStore(object):
    def __init__(self, context=None, default_host=None):
        self._context = context or {}
        self._host_dict = {}
        self._default_host = default_host

    def add_host(self, host_url, host_name=None):
        host_url = self._build_actual_url(host_url)
        host_name = host_name or host_url
        self._host_dict.update({host_name: host_url})

    def generate_js_link(self, js_name, js_host=None):
        js_host = js_host or self._default_host
        host_url = self._host_dict.get(js_host)
        if not host_url:
            if js_host:
                host_url = self._build_actual_url(js_host)
            else:
                raise ValueError('No host is assigned.')
        return '{}/{}.js'.format(host_url, js_name)

    def _build_actual_url(self, host_url):
        host_url = host_url.format(**self._context).rstrip('/')
        return host_url

    @staticmethod
    def from_hosts(context, hosts, default_host):
        hs = HostStore(context=context, default_host=default_host)
        for k, v in hosts.items():
            hs.add_host(v, k)
        return hs
