from .containers import RowContainer


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
        self.add_widget(chart_obj, name=name)
        return self

    def add(self, achart_or_charts):
        if not isinstance(achart_or_charts, (list, tuple, set)):
            achart_or_charts = achart_or_charts,  # Make it a sequence
        for c in achart_or_charts:
            self.add_chart(chart_obj=c)
        return self
