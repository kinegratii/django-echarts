from collections import OrderedDict
from itertools import zip_longest
from typing import Dict, Generator, Tuple, Any, List, Union


class LayoutCfg:
    __slots__ = ['ww', 'wh', 'span', 'offset']

    def __init__(self, ww: str = '', wh: str = '', span: int = 0, offset: int = 0):
        self.ww = ww
        self.wh = wh
        self.span = span
        self.offset = offset

    def __str__(self):
        return f'<LCfg: col-md-{self.span}>'


COL_TOTAL = 12


class ContainerBase:
    """A container containing some widgets."""

    def __init__(self, *args, **kwargs):
        self._widgets = OrderedDict()
        self._layouts = {}  # type: Dict[str,LayoutCfg]
        self.div_class = kwargs.get('div_class', '')
        self._layout_str = ''

    def add_widget(self, widget, name: str = None, width: str = "", height: str = "", span: int = 0,
                   first: bool = False):
        """Add a widget in this container widget.
        If first set to True, insert at the beginning position in list."""
        name = name or 'c{}'.format(len(self._widgets))
        self._widgets[name] = widget
        lc = LayoutCfg(ww=width, wh=height, span=span)
        self._layouts[name] = lc
        if first:
            self._widgets.move_to_end(name, False)
        return self

    def auto_layout(self):
        """Auto compute col spans for each widget."""
        pass

    def __iter__(self):
        """Iter each widget."""
        for chart in self._widgets.values():
            yield chart

    def __len__(self):
        return len(self._widgets)

    def __getitem__(self, item):
        if isinstance(item, int):
            # c[1], Just compatible with Page
            return list(self._widgets.values())[item]
        return self._widgets[item]

    def iter_layout(self) -> Generator[Tuple[Any, LayoutCfg], None, None]:
        """Iter each widget and its layout config."""
        self.auto_layout()
        for name, widget in self._widgets.items():
            yield widget, self._layouts.get(name, LayoutCfg())


class Container(ContainerBase):
    """General container."""

    def __init__(self, *args, div_class: str = '', **kwargs):
        super().__init__(div_class=div_class, *args, **kwargs)


class RowContainer(ContainerBase):
    """A row container."""

    def set_spans(self, spans: Union[int, List[int]]):
        """Set span value for each widget.
        This should be called after all widgets is add."""
        if isinstance(spans, int):
            if spans == 0:
                span_list = [int(12 / len(self._widgets))] * len(self._layouts)
            else:
                span_list = [spans] * len(self._layouts)
        else:
            span_list = spans
        for lc, span in zip_longest(self._layouts.values(), span_list):
            if lc is None:
                continue
            lc.span = span or COL_TOTAL

    def auto_layout(self):
        """Auto compute col spans for each widget."""
        item_num = len([lc for lc in self._layouts.values() if lc.span == 0])
        if item_num == 0:  # Each widget has its own span.
            return
        total_span = COL_TOTAL - sum([lc.span for lc in self._layouts.values() if lc.span])
        col_span = int(total_span / item_num)
        for lc in self._layouts.values():
            if lc.span == 0:
                lc.span = col_span
            lc.ww = '100%'

    def get_spans(self) -> Tuple[int]:
        return tuple([lc.span for lc in self._layouts.values()])
