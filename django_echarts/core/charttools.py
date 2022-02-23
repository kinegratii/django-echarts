from collections import OrderedDict
from typing import List, Optional


class ChartsConstants:
    AUTO_WIDTH = '100%'


def _flat(ele):
    if hasattr(ele, 'js_dependencies'):
        if isinstance(ele.js_dependencies, list):
            return ele.js_dependencies
        if hasattr(ele.js_dependencies, 'items'):
            return list(ele.js_dependencies.items)  # pyecharts.commons.utils.OrderedSet
        raise ValueError('Can not parse js_dependencies.')
    if isinstance(ele, (list, tuple, set)):
        return ele
    return ele,


def merge_js_dependencies(*chart_or_name_list, enable_theme=False):
    front_required_items = ['echarts']
    front_optional_items = ['echartsgl']
    dependencies = []
    fist_items = set()

    def _add(_item):
        if _item in front_required_items:
            pass
        elif _item in front_optional_items:
            fist_items.add(_item)
        elif _item not in dependencies:
            dependencies.append(_item)

    for d in chart_or_name_list:
        for _d in _flat(d):
            _add(_d)
        if enable_theme and hasattr(d, 'theme'):
            _add(d.theme)
    return front_required_items + [x for x in front_optional_items if x in fist_items] + dependencies


class DJEChartInfo:
    """The meta-data class for a chart."""
    __slots__ = ['name', 'title', 'description', 'url', 'selected', 'parent_name', 'top', 'tags', 'extra']

    def __init__(self, name: str, title: str = None, description: str = None, url: str = None,
                 selected: bool = False, parent_name: str = None, top: int = 0, tags=None, extra=None):
        self.name = name
        self.title = title or self.name
        self.description = description or ''
        self.url = url
        self.selected = selected
        self.top = top
        self.parent_name = parent_name
        self.tags = tags or []
        self.extra = extra or {}

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'<ChartInfo {self.name}>'


class ChartManagerMixin:
    """The backend for the store of chart info."""

    def add_chart_info(self, info: DJEChartInfo):
        pass

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[DJEChartInfo]:
        pass

    def get_or_none(self, name: str) -> Optional[DJEChartInfo]:
        pass


class LocalChartManager(ChartManagerMixin):
    def __init__(self):
        self._chart_info_list = []  # type: List[DJEChartInfo]

    def add_chart_info(self, info: DJEChartInfo):
        self._chart_info_list.append(info)

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[DJEChartInfo]:
        chart_info_list = [info for info in self._chart_info_list if not with_top or info.top]
        if keyword:
            def _filter(_item):
                return keyword in _item.title or keyword in _item.tags

            chart_info_list = list(filter(_filter, chart_info_list))
        if with_top:
            chart_info_list.sort(key=lambda x: x.top)
        return chart_info_list

    def get_or_none(self, name: str) -> Optional[DJEChartInfo]:
        for info in self._chart_info_list:
            if info.name == name:
                return info


class NamedCharts:
    """
    A data structure class containing multiple named charts.
    """

    def __init__(self, page_title: str = 'EChart', col_chart_num: int = 1):
        self.page_title = page_title
        self._charts = OrderedDict()
        self._col_chart_num = col_chart_num

    @property
    def col_chart_num(self):
        return self._col_chart_num

    def add_chart(self, chart, name=None):
        name = name or self._next_name()
        if hasattr(chart, 'width'):
            chart.width = '100%'
        self._charts[name] = chart
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
            self.add_chart(chart=c)
        return self

    # Chart-like feature

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self)

    @classmethod
    def from_charts(cls, *charts):
        mc = cls()
        for chart in charts:
            mc.add_chart(chart)
        return mc


class ChartPageContainer:
    """A multiple charts container including DJEChartInfo data.Compatible with NamedCharts.
    """

    def __init__(self, col_chart_num: int = 1, chart_col_span: int = 6, info_col_span: int = 6):
        self._chart_dic = OrderedDict()
        self._info_dic = OrderedDict()
        self._col_chart_num = col_chart_num

        self._card_col_span = int(12 / col_chart_num)
        if col_chart_num > 1:
            self._chart_col_span = 8
            self._info_col_span = 4
        else:
            self._chart_col_span = chart_col_span
            self._info_col_span = info_col_span

    @property
    def col_chart_num(self):
        """The total of every row."""
        return self._col_chart_num

    @property
    def card_col_span(self):
        return self._card_col_span

    @property
    def chart_col_span(self):
        return self._chart_col_span

    @property
    def info_col_span(self):
        return self._info_col_span

    @property
    def charts(self) -> List:
        return list(self._chart_dic.values())

    def add(self, chart_obj, info: DJEChartInfo):
        if hasattr(chart_obj, 'width'):
            chart_obj.width = '100%'
        self._chart_dic[info.name] = chart_obj
        self._info_dic[info.name] = info

    def __iter__(self):
        for chart_name, chart_obj in self._chart_dic.items():
            yield chart_obj, self._info_dic.get(chart_name)

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self._chart_dic.values())
