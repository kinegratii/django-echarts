from collections import OrderedDict
from typing import Optional, Any, Tuple

from .articles import ChartInfo


class NamedCharts:
    """
    A data structure class containing multiple named charts.
    is_combine: if True, the collection <all> will not contains this chart.


    """
    widget_type = 'NamedCharts'

    def __init__(self, page_title: str = 'EChart', col_chart_num: int = 1, is_combine: bool = False):
        self.page_title = page_title
        self._charts = OrderedDict()
        self._col_chart_num = col_chart_num
        self.is_combine = is_combine
        self.has_ref = is_combine

    @property
    def col_chart_num(self):
        return self._col_chart_num

    def add_chart(self, chart_obj, name=None):
        name = name or self._next_name()
        if hasattr(chart_obj, 'width'):
            chart_obj.width = '100%'
        self._charts[name] = chart_obj
        return self

    def _next_name(self):
        return 'c{}'.format(len(self))

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
            self.add_chart(chart_obj=c)
        return self

    # Chart-like feature

    @classmethod
    def from_charts(cls, *charts):
        mc = cls()
        for chart in charts:
            mc.add_chart(chart)
        return mc


# l1-l12 r1-r12 t1-t12 b1-b12 f1-f12 a s1-s12

class WidgetGetterMixin:
    def resolve_chart_widget(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Return a pycharts chart object."""
        pass

    def resolve_html_widget(self, name: str) -> Any:
        """Return a html widget object."""
        pass


class ChartWidget:
    def __init__(self, chart_id, width, height):
        self.chart_id = chart_id
        self.width = width
        self.height = height

    @classmethod
    def from_chart_obj(cls, chart_obj):
        pass


