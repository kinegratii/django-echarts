import re
from collections import OrderedDict
from typing import List, Union, Tuple, Any, Optional

from .articles import ChartInfo
from .containers import RowContainer, Container


class LayoutOpts:
    """Layout for user defined.
    """
    __slots__ = ['pos', 'span', 'start']

    # l=left,r=right,s=stripped,t=top,b=bottom,f=full
    _defaults = {'l': 8, 'r': 8, 's': 8, 't': 6, 'b': 6, 'f': 12}

    _rm = re.compile(r'([lrtbfsa])(([1-9]|(1[12]))?)')

    def __init__(self, pos: str = 'r', span: int = 8):
        self.pos = pos
        self.span = span
        self.start = pos in 'rb'

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

    def stripped_layout(self) -> 'LayoutOpts':
        if self.pos == 'r':
            return LayoutOpts(pos='l', span=self.span)
        elif self.pos == 'l':
            return LayoutOpts(pos='r', span=self.span)
        else:
            return self

    def __str__(self):
        return f'<LOptions:{self.pos},{self.span}>'


class WidgetGetterMixin:
    def resolve_chart_widget(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Return a pycharts chart object."""
        pass

    def resolve_html_widget(self, name: str) -> Any:
        """Return a html widget object."""
        pass


class WidgetCollection(Container):
    """A row-list-container"""
    widget_type = 'Collection'

    def __init__(self, name: str, title: str = None, layout: Union[str, LayoutOpts] = 'a'):
        super().__init__()
        self.name = name
        self.title = title
        self._user_defined_layout = LayoutOpts.from_label(layout)
        self._ref_config_list = []  # type: List
        self._row_no = 0

    def start_(self):
        self._widgets = OrderedDict()
        self._row_no = 0
        return self

    def add_chart_widget(self, chart_name: str, layout: str = 'l8'):
        self._ref_config_list.append([True, layout, chart_name])
        return self

    def add_html_widget(self, widget_names: List, layout: str = 'f'):
        self._ref_config_list.append([False, layout, *widget_names])

    def auto_mount(self, widget_container: WidgetGetterMixin):
        for is_chart, layout_str, *names in self._ref_config_list:
            if is_chart:
                chart_name = names[0]
                chart_obj, _, info = widget_container.resolve_chart_widget(chart_name)
                self.pack_chart_widget(chart_obj, info, row_no=self._row_no)
            else:
                widget_list = [widget_container.resolve_html_widget(name) for name in names]
                self.pack_html_widget(widget_list)

    def pack_chart_widget(self, chart_obj, info: ChartInfo, ignore_ref: bool = True, layout: str = 'l8',
                          row_no: int = 0):
        r_layout = self.compute_layout(LayoutOpts.from_label(layout))
        if isinstance(chart_obj, RowContainer):
            if getattr(chart_obj, 'has_ref', False) and ignore_ref:
                return
            row_widget = chart_obj
            row_widget.add_widget(info, first=r_layout.start)
        else:
            # pyecharts.charts.Base
            row_widget = RowContainer()
            row_widget.add_widget(chart_obj, span=r_layout.span)
            row_widget.add_widget(info, first=r_layout.start)
        self.add_widget(row_widget)
        self._row_no += 1

    def pack_html_widget(self, widget_list: List, layout: str = 'f', row_no: int = 0):
        row_widget = RowContainer()
        for widget in widget_list:
            row_widget.add_widget(widget)
        self.add_widget(row_widget)
        self._row_no += 1

    def compute_layout(self, row_layout: LayoutOpts):
        if self._user_defined_layout.pos == 'a':
            return row_layout
        elif self._user_defined_layout.pos == 's':
            if self._row_no % 2 == 1:
                return row_layout.stripped_layout()
            else:
                return row_layout
        else:
            return row_layout
