from collections import OrderedDict
from typing import Dict, Generator, Tuple, Any


class LayoutCfg:
    def __init__(self, ww: str = '', wh: str = '', span: int = 0, offset: int = 0):
        self.ww = ww
        self.wh = wh
        self.span = span
        self.offset = offset

    @property
    def widget_style(self):
        s = 'style="width:{};height:{};"'
        sl = []
        if self.ww:
            sl.append(f'width:{self.ww};')
        if self.wh:
            sl.append(f'height:{self.wh};')
        if sl:
            return ' style="{}"'.format(''.join(sl))
        else:
            return ''


class CLayoutOpts:
    def __init__(self, pos: str, span: int = 0):
        self.pos = pos
        self.span = span


class RowMixin:
    """A container rendered as a row-class div."""

    def __init__(self, *args, **kwargs):
        self._widgets = OrderedDict()
        self._layouts = {}  # type: Dict[str,LayoutCfg]

    def add_widget(self, widget, name: str = None, width: str = "", height: str = "", span: int = 0):
        name = name or 'c{}'.format(len(self._widgets))
        self._widgets[name] = widget
        lc = LayoutCfg(ww=width, wh=height, span=span)
        self._layouts[name] = lc
        return self

    def auto_layout(self):
        item_num = len([lc for lc in self._layouts.values() if lc.span == 0])
        total_span = 12 - sum([lc.span for lc in self._layouts.values() if lc.span])
        col_span = int(total_span / item_num)
        for lc in self._layouts.values():
            if lc.span == 0:
                lc.span = col_span
            lc.ww = '100%'

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


class RowContainer(RowMixin):
    """A row container."""

    def __init__(self, *args, **kwargs):
        super(RowContainer, self).__init__(*args, **kwargs)

    # def add_widget(self, widget, name: str = None, width: str = "", height: str = "", span: int = 0):
    #     name = name or 'c{}'.format(len(self._widgets))
    #     self._widgets[name] = widget
    #     lc = LayoutCfg(ww=width, wh=height, span=span)
    #     self._layouts[name] = lc
    #     return self

    # def auto_layout(self):
    #     col_span = int(12 / len(self._widgets))
    #     for lc in self._layouts.values():
    #         if lc.span == 0:
    #             lc.span = col_span
    #         lc.ww = '100%'

    # def iter_layout(self) -> Generator[Tuple[Any, LayoutCfg], None, None]:
    #     """Iter each widget and its layout config."""
    #     self.auto_layout()
    #     for name, widget in self._widgets.items():
    #         yield widget, self._layouts.get(name, LayoutCfg())

    # def __iter__(self):
    #     """Iter each widget."""
    #     for chart in self._widgets.values():
    #         yield chart
    #
    # def __len__(self):
    #     return len(self._widgets)
    #
    # def __getitem__(self, item):
    #     if isinstance(item, int):
    #         # c[1], Just compatible with Page
    #         return list(self._widgets.values())[item]
    #     return self._widgets[item]
