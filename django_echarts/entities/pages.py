from collections import OrderedDict
from abc import abstractmethod
from typing import List, Union, Tuple, Any, Optional
import warnings

from .uri import EntityURI
from .articles import ChartInfo
from .containers import RowContainer, Container
from .layouts import LayoutOpts, TYPE_LAYOUT_OPTS, any2layout


class WidgetGetterMixin:

    @abstractmethod
    def get_chart_and_info(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Return a pycharts chart object."""
        warnings.warn('This method is deprecated, use get_chart_and_info_by_uri instead.', DeprecationWarning,
                      stacklevel=2)
        pass

    @abstractmethod
    def get_html_widget(self, name: str) -> Any:
        """Return a html widget object."""
        warnings.warn('This method is deprecated, use get_widget_by_uri instead.', DeprecationWarning, stacklevel=2)
        pass

    @abstractmethod
    def get_widget_by_name(self, name: str) -> Any:
        warnings.warn('This method is deprecated, use get_widget_by_uri instead.', DeprecationWarning, stacklevel=2)
        pass

    @abstractmethod
    def get_chart_and_info_by_uri(self, uri: EntityURI) -> Tuple[Any, bool, Optional[ChartInfo]]:
        pass

    @abstractmethod
    def get_widget_by_uri(self, uri: EntityURI):
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
        self._ref_config_list.append([True, layout, EntityURI.from_str(chart_name, catalog='chart')])
        return self

    def add_html_widget(self, widget_names: List, layout: TYPE_LAYOUT_OPTS = 0):
        widget_uri_list = [EntityURI.from_str(name, catalog='widget') for name in widget_names]
        self._ref_config_list.append([False, layout, *widget_uri_list])

    def auto_mount(self, widget_container: WidgetGetterMixin):
        self.start_()
        for is_chart, layout_str, *uri_list in self._ref_config_list:
            if is_chart:
                chart_uri = uri_list[0]
                chart_obj, _, info = widget_container.get_chart_and_info_by_uri(chart_uri)
                self.pack_chart_widget(chart_obj, info, row_no=self._row_no)
            else:
                widget_list = [widget_container.get_widget_by_uri(uri) for uri in uri_list]
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
