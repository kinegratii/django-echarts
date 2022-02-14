from typing import List, Optional


class DJEChartInfo:
    """The meta-data class for a chart."""
    __slots__ = ['name', 'title', 'description', 'url', 'selected', 'parent_name', 'top', 'tags']

    def __init__(self, name: str, title: str = None, description: str = None, url: str = None,
                 selected: bool = False, parent_name: str = None, top: int = 0, tags=None):
        self.name = name
        self.title = title or self.name
        self.description = description or ''
        self.url = url
        self.selected = selected
        self.top = top
        self.parent_name = parent_name
        self.tags = tags or []

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
