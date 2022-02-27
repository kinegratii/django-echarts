import re
from collections import OrderedDict
from typing import List, Optional, Union


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

    def __init__(self, page_title: str = 'EChart', col_chart_num: int = 1, is_combine: bool = False):
        self.page_title = page_title
        self._charts = OrderedDict()
        self._col_chart_num = col_chart_num
        self.is_combine = is_combine

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


# l1-l12 r1-r12 t1-t12 b1-b12 f1-f12 a s1-s12
class ChartPosition:
    LEFT = 'l'  # left
    RIGHT = 'r'  # right
    TOP = 't'  # top
    BOTTOM = 'b'  # bottom
    FULL = 'f'  # full
    # The following opts are only used in collection, not row.
    AUTO = 'a'  # auto
    STRIPPED = 's'  # stripped


class LayoutOpts:
    """
    Recommend layout: l8 l9 r8 r9 t6 t12 b6 b12 f4 f6 f12 a s8 s9
    """
    TOTAL_COLS = 12
    __slots__ = ['chart_pos', 'chart_span', 'info_span', 'start', 'end']

    _defaults = {'l': 8, 'r': 8, 's': 8, 't': 6, 'b': 6, 'f': 12}

    _rm = re.compile(r'([lrtbfsa])(([1-9]|(1[12]))?)')

    def __init__(self, chart_pos: str = ChartPosition.LEFT, chart_span: int = 8, info_span: int = 4):
        if len(chart_pos) > 1:
            chart_pos = chart_pos[0]
        self.chart_pos = chart_pos
        self.chart_span = chart_span
        if chart_pos in 'lras':
            if chart_span + info_span != LayoutOpts.TOTAL_COLS:
                info_span = LayoutOpts.TOTAL_COLS - chart_span
        self.info_span = info_span
        # start/end for info
        self.start = chart_pos in (ChartPosition.RIGHT, ChartPosition.BOTTOM)
        self.end = chart_pos in (ChartPosition.LEFT, ChartPosition.TOP)

    @classmethod
    def from_label(cls, label: str):
        m = LayoutOpts._rm.match(label)
        if m:
            pos, cols = m.group(1), m.group(2)
            if cols is None:
                cols = LayoutOpts._defaults.get(pos, 8)
            else:
                cols = int(cols)
            return cls(pos, cols)
        else:
            raise ValueError(f'This layout can not be parsed: {label}')

    def __str__(self):
        return f'<LOptions:{self.chart_pos},{self.chart_span}, {self.info_span}>'


class ChartCollection:
    """A multiple charts container including DJEChartInfo data.Compatible with NamedCharts.
    """

    def __init__(self, name: str = None, layout: Union[str, LayoutOpts] = None):
        self.name = name
        self._name_list = []  # type: List[str]
        self._chart_dic = []
        self._info_dic = []  # type: List[DJEChartInfo]
        # expose the following for render
        self._row_layout_opts_list = []  # type: List[LayoutOpts]
        self.card_span = LayoutOpts.TOTAL_COLS
        # Handle user input
        if isinstance(layout, str):
            self._user_layout = LayoutOpts.from_label(layout)  # type: LayoutOpts
        else:
            self._user_layout = layout or LayoutOpts(ChartPosition.LEFT, 8, 4)  # type: LayoutOpts

    def adjust_layout(self):
        c_opts = self._user_layout
        if c_opts.chart_pos == ChartPosition.AUTO:
            pass
        elif c_opts.chart_pos in (ChartPosition.STRIPPED, ChartPosition.LEFT, ChartPosition.RIGHT):
            self._row_layout_opts_list = []
            for i, name in enumerate(self._name_list):
                c_span, i_span = c_opts.chart_span, LayoutOpts.TOTAL_COLS - c_opts.chart_span
                if c_opts.chart_pos == ChartPosition.STRIPPED:
                    if i % 2 == 0:
                        pos = ChartPosition.LEFT
                    else:
                        pos = ChartPosition.RIGHT
                else:
                    pos = c_opts.chart_pos
                self._row_layout_opts_list.append(LayoutOpts(pos, c_span, i_span))
        elif c_opts.chart_pos == ChartPosition.FULL:
            self._row_layout_opts_list = [LayoutOpts(ChartPosition.FULL, c_opts.chart_span)] * len(self._name_list)
            self.card_span = c_opts.chart_span
        elif c_opts.chart_pos in (ChartPosition.TOP, ChartPosition.BOTTOM):
            self._row_layout_opts_list = [LayoutOpts(ChartPosition.FULL, LayoutOpts.TOTAL_COLS)] * len(self._name_list)
        else:
            pass
        return self

    # @property
    # def _collection_layout_opts(self):
    #     return self._collection_layout_opts

    @property
    def charts(self) -> List:
        return self._chart_dic

    def add(self, chart_obj, info: DJEChartInfo, ignore_chart_type: bool = False):
        if isinstance(chart_obj, NamedCharts) and chart_obj.is_combine:
            if ignore_chart_type:
                return self
            else:
                raise TypeError(f'{info.name} :ChartCollection can not add a NamedCharts with is_combine=True')
        if hasattr(chart_obj, 'width'):
            chart_obj.width = '100%'

        self._name_list.append(info.name)
        self._chart_dic.append(chart_obj)
        self._info_dic.append(info)
        return self

    def auto_layout(self):
        pass

    def iter_for_layout(self):
        for chart_obj, chart_info, row_layout_ops in zip(self._chart_dic, self._info_dic, self._row_layout_opts_list):
            yield chart_obj, chart_info, row_layout_ops

    def __iter__(self):
        for chart_obj, chart_info in zip(self._chart_dic, self._info_dic):
            yield chart_obj, chart_info

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self._chart_dic)
