import re
from collections import OrderedDict
from typing import List, Union, Dict, Optional, Any, Tuple

from .articles import ChartInfo


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

    def __init__(self, chart_pos: str = ChartPosition.LEFT, chart_span: int = 8, info_span: int = 4,
                 chart_num: int = 1):
        if len(chart_pos) > 1:
            chart_pos = chart_pos[0]
        self.chart_pos = chart_pos
        self.chart_span = chart_span
        if chart_pos in 'lras':
            if chart_num == 1 and chart_span + info_span < LayoutOpts.TOTAL_COLS:
                info_span = LayoutOpts.TOTAL_COLS - chart_span
            elif chart_num > 1:
                info_span = 12
        self.info_span = info_span
        # start/end for info
        self.start = chart_pos in (ChartPosition.RIGHT, ChartPosition.BOTTOM)
        self.end = chart_pos in (ChartPosition.LEFT, ChartPosition.TOP)

    @classmethod
    def from_label(cls, label: str):
        m = LayoutOpts._rm.match(label)
        if m:
            pos, cols = m.group(1), m.group(2)
            if cols is None or cols == '':
                cols = LayoutOpts._defaults.get(pos, 8)
            else:
                cols = int(cols)
            return cls(pos, cols)
        else:
            raise ValueError(f'This layout can not be parsed: {label}')

    def __str__(self):
        return f'<LOptions:{self.chart_pos},{self.chart_span}, {self.info_span}>'


class WidgetGetterMixin:
    def resolve_chart_widget(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Return a pycharts chart object."""
        pass

    def resolve_html_widget(self, name: str) -> Any:
        """Return a html widget object."""
        pass


class WidgetCollection:
    """
    wc = WidgetCollection()
    wc.add_widget_ref(chart_name, widget_names=)

    """

    widget_type = 'Collection'

    def __init__(self, name: str, title: str = None, layout: Union[str, LayoutOpts] = 'a'):
        self.name = name
        self.title = title
        self._user_defined_layout = LayoutOpts.from_label(layout)
        # [[is_chart, layout, name1, name2, name3,...]]
        self._ref_config_list = []  # type: List

        self._packed_matrix = []  # type: List[List]
        self._charts = []

    def add_chart(self, chart_name: str, layout: str = 'l8'):
        self._ref_config_list.append([True, layout, chart_name])
        return self

    def add_html_widget(self, widget_names: List, layout: str = 'f'):
        self._ref_config_list.append([False, layout, *widget_names])

    def auto_mount(self, widget_container: WidgetGetterMixin):
        for is_chart, layout_str, *names in self._ref_config_list:
            if is_chart:
                chart_name = names[0]
                chart_obj, _, info = widget_container.resolve_chart_widget(chart_name)
                self.pack_chart_widget(chart_obj, info)
            else:
                widget_list = [widget_container.resolve_html_widget(name) for name in names]
                self.pack_html_widget(widget_list)

    def pack_chart_widget(self, chart_obj, info: ChartInfo, ignore_ref: bool = True, layout: str = 'l8'):
        self._charts.append(chart_obj)
        if isinstance(chart_obj, NamedCharts):
            if chart_obj.has_ref and ignore_ref:
                return
                # raise TypeError(f'{info.name} :ChartCollection can not add a NamedCharts with is_combine=True')
            chart_widget = list(chart_obj)
        else:
            chart_widget = [chart_obj]
        row_data = []
        r_layout = LayoutOpts.from_label(layout)
        if r_layout.start:
            row_data.append((info, r_layout.info_span))
        for widget in chart_widget:
            row_data.append((widget, r_layout.chart_span))
        if r_layout.end:
            row_data.append((info, r_layout.info_span))
        self._packed_matrix.append(row_data)

    def pack_html_widget(self, widget_list: List, layout: str = 'f'):
        span = int(12 / len(widget_list))
        row_data = [(widget, span) for widget in widget_list]
        self._packed_matrix.append(row_data)

    @property
    def packed_matrix(self):
        return self._packed_matrix

    @property
    def charts(self):
        return self._charts

    @property
    def js_dependencies(self):
        return merge_js_dependencies(*self.charts)
