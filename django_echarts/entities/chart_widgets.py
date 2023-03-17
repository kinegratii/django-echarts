import warnings
from dataclasses import dataclass, field
from .containers import RowContainer


@dataclass
class BlankChart:
    """A interface class for tests only."""
    width: str = '900px'
    height: str = '500px'
    renderer: str = 'canvas'
    page_title: str = 'Blank Chart'
    theme: str = 'white'
    chart_id: str = 'dje_blank'
    options: dict = field(default_factory=dict)
    js_dependencies: list = field(default_factory=lambda: ['echarts'])  # Use Simplified format.
    geojson: dict = None  # added by django-echarts

    def __post_init__(self):
        self._is_geo_chart = False

    def dump_options(self) -> str:
        return "{}"


class NamedCharts(RowContainer):
    """
    A data structure class containing multiple named charts.
    is_combine: if True, the collection <all> will not contains this chart.


    """

    def __init__(self, page_title: str = 'EChart', col_chart_num: int = 0, is_combine: bool = False):
        super().__init__()
        self.page_title = page_title
        self._col_chart_num = col_chart_num
        self.is_combine = is_combine
        self.has_ref = is_combine

    def auto_layout(self):
        if self._col_chart_num != 0:
            span = int(12 / self._col_chart_num)
            self.set_spans(span)
        else:
            super().auto_layout()

    def add_chart(self, chart_obj, name=None):
        warnings.warn('This method is deprecated. Use NamedChart.add_widget instead.', DeprecationWarning, stacklevel=2)
        self.add_widget(chart_obj, name=name)
        return self

    def add(self, achart_or_charts):
        warnings.warn('This method is deprecated. Use NamedChart.add_widget instead.', DeprecationWarning, stacklevel=2)
        if not isinstance(achart_or_charts, (list, tuple, set)):
            achart_or_charts = achart_or_charts,  # Make it a sequence
        for c in achart_or_charts:
            self.add_widget(c)
        return self
