from collections import OrderedDict
from typing import List, Union, Tuple, Any, Optional

from .articles import ChartInfo
from .containers import RowContainer, Container
from .layouts import LayoutOpts, TYPE_LAYOUT_OPTS, any2layout


class WidgetGetterMixin:
    def get_chart_and_info(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Return a pycharts chart object."""
        pass

    def get_html_widget(self, name: str) -> Any:
        """Return a html widget object."""
        pass

    def get_widget_by_name(self, name: str) -> Any:
        pass


class WidgetCollection(Container):
    """A row-list-container"""
    widget_type = 'Collection'

    def __init__(self, name: str, title: str = None, layout: TYPE_LAYOUT_OPTS = 'a'):
        super().__init__()
        self.name = name
        self.title = title
        self._user_defined_layout = any2layout(layout)
        self._ref_config_list = []  # type: List
        self._row_no = 0

    def start_(self):
        self._widgets = OrderedDict()
        self._row_no = 0
        return self

    def add_chart_widget(self, chart_name: str, layout: TYPE_LAYOUT_OPTS = 'l8'):
        self._ref_config_list.append([True, layout, chart_name])
        return self

    def add_html_widget(self, widget_names: List, layout: TYPE_LAYOUT_OPTS = 0):
        self._ref_config_list.append([False, layout, *widget_names])

    def auto_mount(self, widget_container: WidgetGetterMixin):
        self.start_()
        for is_chart, layout_str, *names in self._ref_config_list:
            if is_chart:
                chart_name = names[0]
                chart_obj, _, info = widget_container.get_chart_and_info(chart_name)
                self.pack_chart_widget(chart_obj, info, row_no=self._row_no)
            else:
                widget_list = [widget_container.get_widget_by_name(name) for name in names]
                self.pack_html_widget(widget_list)

    def pack_chart_widget(self, chart_obj, info: ChartInfo, ignore_ref: bool = True, layout: str = 'l8',
                          row_no: int = 0):
        r_layout = self.compute_layout(any2layout(layout))
        if isinstance(chart_obj, RowContainer):
            if getattr(chart_obj, 'has_ref', False) and ignore_ref:
                return
            row_widget = chart_obj
            row_widget.set_spans(0)
            row_widget.add_widget(info, first=r_layout.start, span=12)
        else:
            # pyecharts.charts.Base
            row_widget = RowContainer()
            row_widget.add_widget(chart_obj, span=r_layout.spans[0])
            row_widget.add_widget(info, first=r_layout.start)
        self.add_widget(row_widget)
        self._row_no += 1

    def pack_html_widget(self, widget_list: List, spans: Union[int, List[int]] = 0, row_no: int = 0):
        row_widget = RowContainer()
        for widget in widget_list:
            row_widget.add_widget(widget)
        if spans != 0:
            row_widget.set_spans(spans)
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
