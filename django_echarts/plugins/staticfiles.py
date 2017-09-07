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

    def generate_js_link(self, js_name):
        return '{0}/{1}.js'.format(self._host, js_name)


class HostStore(HostMixin):
    def __init__(self, echarts_lib_name_or_host, echarts_map_name_or_host,
                 context=None, **kwargs):
        context = context or {}

        self._lib_js_host = Host(echarts_lib_name_or_host, context=context, host_lookup=ECHARTS_LIB_HOSTS, **kwargs)
        self._map_js_host = Host(echarts_map_name_or_host, context=context, host_lookup=ECHARTS_MAP_HOSTS, **kwargs)

    def generate_js_link(self, js_name):
        if is_lib_or_map_js(js_name):
            return self._lib_js_host.generate_js_link(js_name)
        else:
            return self._map_js_host.generate_js_link(js_name)


if __name__ == '__main__':
    m_context = {
        'STATIC_URL': '/static/',
        'echarts_version': '3.7.0'
    }
    s1 = HostStore('bootcdn', m_context)
    print(s1.generate_js_link('echarts.min'))  # https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js

    s2 = HostStore('{STATIC_URL}echarts', m_context)
    print(s2.generate_js_link('echarts.min'))  # /static/echarts/echarts.min.js
