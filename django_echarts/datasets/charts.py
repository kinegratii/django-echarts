# coding=utf8

from django_echarts.utils.interfaces import merge_js_dependencies


class MCharts:
    """
    A list containing multiple named charts.
    """

    def __init__(self, page_title='EChart', **kwargs):
        self.page_title = page_title
        self._names = []
        self._charts = []

        for name, chart in kwargs.items():
            self.add_chart(chart=chart, name=name)

    def add_chart(self, chart, name=None):
        name = name or self._next_name()
        self._names.append(name)
        self._charts.append(chart)
        return self

    def __iter__(self):
        for chart in self._charts:
            yield chart

    def __contains__(self, item):
        return item in self._names

    def __getattr__(self, item):
        try:
            i = self._names.index(item)
            return self._charts[i]
        except ValueError:
            return super().__getattr__(item)

    def _next_name(self):
        return 'c{}'.format(len(self._charts))

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self)

    @classmethod
    def from_charts(cls, *args):
        mc = cls()
        for c in args:
            mc.add_chart(c)
        return mc
