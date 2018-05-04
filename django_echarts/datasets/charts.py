# coding=utf8
from collections import OrderedDict
from django_echarts.utils.interfaces import merge_js_dependencies


class NamedCharts:
    """
    A data structure class containing multiple named charts.
    """

    def __init__(self, page_title='EChart', **kwargs):
        self.page_title = page_title
        self._charts = OrderedDict()
        for k, v in kwargs.items():
            self.add_chart(chart=v, name=k)

    def add_chart(self, chart, name=None):
        name = name or self._next_name()
        self._charts[name] = chart
        return self

    def _next_name(self):
        return 'c{}'.format(len(self._charts))

    # List-like feature

    def __iter__(self):
        for chart in self._charts.values():
            yield chart

    def __len__(self):
        return len(self._charts)

    # Dict-like feature

    def __contains__(self, item):
        return item in self._charts

    def __getitem__(self, item):
        if isinstance(item, int):
            # c[1], Just compatible with Page
            return list(self._charts.values())[item]
        return self._charts[item]

    def __setitem__(self, key, value):
        self._charts[key] = value

    # Compatible

    def add(self, achart_or_charts):
        if not isinstance(achart_or_charts, (list, tuple, set)):
            achart_or_charts = achart_or_charts,  # Make it a sequence
        for c in achart_or_charts:
            self.add_chart(chart=c)

    # Chart-like feature

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self)

    @classmethod
    def from_charts(cls, *args):
        mc = cls()
        for c in args:
            mc.add_chart(c)
        return mc
