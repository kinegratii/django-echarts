# coding=utf8
"""A javascript host manager.
"""

from __future__ import unicode_literals


class HostStore(object):
    HOSTS = {
        'pyecharts': 'https://chfw.github.io/jupyter-echarts/echarts',  # TODO Use pyecharts.constants.DEFAULT_HOST
        'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version}',
        'npmcdn': 'https://unpkg.com/echarts@{echarts_version}/dist',
        'bootcdn': 'https://cdn.bootcss.com/echarts/{echarts_version}'
    }

    def __init__(self, name_or_host, context=None, **kwargs):
        context = context or {}
        host = self.HOSTS.get(name_or_host, name_or_host)
        try:
            self._host = host.format(**context).rstrip('/')
        except KeyError as e:
            self._host = None
            raise KeyError('The "{0}" value is not applied for the host.'.format(*e.args))

    def generate_js_link(self, js_name):
        return '{0}/{1}.js'.format(self._host, js_name)

    @property
    def host_url(self):
        return self._host


if __name__ == '__main__':
    m_context = {
        'STATIC_URL': '/static/',
        'echarts_version': '3.7.0'
    }
    s1 = HostStore('bootcdn', m_context)
    print(s1.generate_js_link('echarts.min'))  # https://cdn.bootcss.com/echarts/3.7.0/echarts.min.js

    s2 = HostStore('{STATIC_URL}echarts', m_context)
    print(s2.generate_js_link('echarts.min'))  # /static/echarts/echarts.min.js
