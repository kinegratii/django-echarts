from collections import defaultdict
from typing import Dict, Optional, List, Tuple
from .html_widgets import HTMLBase

__all__ = ['ChartInfo', 'ChartInfoManagerMixin', 'LocalChartInfoManager']


class ChartInfo(HTMLBase):
    widget_type = 'InfoCard'
    """The meta-data class for a chart."""
    __slots__ = ['name', 'title', 'description', 'body', 'url', 'selected', 'catalog', 'top', 'tags', 'layout',
                 'extra']

    def __init__(self, name: str, title: str = None, description: str = None, body: str = None, url: str = None,
                 selected: bool = False, catalog: str = None, top: int = 0, tags: List = None, layout: str = None,
                 extra: Dict = None):
        self.name = name
        self.title = title or self.name
        self.description = description or ''
        self.body = body
        self.url = url
        self.selected = selected
        self.top = top
        self.catalog = catalog
        self.tags = tags or []
        self.layout = layout
        self.extra = extra or {}

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'<ChartInfo {self.name}>'


class ChartInfoManagerMixin:
    """The backend for the store of chart info."""

    def add_chart_info(self, info: ChartInfo):
        pass

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[ChartInfo]:
        pass

    def query_group_list(self) -> List[Tuple[str, List[ChartInfo]]]:
        pass

    def get_or_none(self, name: str) -> Optional[ChartInfo]:
        pass

    def count(self) -> int:
        pass


class LocalChartInfoManager(ChartInfoManagerMixin):
    def __init__(self):
        self._chart_info_list = []  # type: List[ChartInfo]

    def add_chart_info(self, info: ChartInfo):
        self._chart_info_list.append(info)

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[ChartInfo]:
        chart_info_list = [info for info in self._chart_info_list if not with_top or info.top]
        if keyword:
            def _filter(_item):
                return keyword in _item.title or keyword in _item.tags

            chart_info_list = list(filter(_filter, chart_info_list))
        if with_top:
            chart_info_list.sort(key=lambda x: x.top)
        return chart_info_list

    def query_group_list(self) -> List[Tuple[str, List[ChartInfo]]]:
        catalog2info = defaultdict(list)
        group_names = []
        for info in self._chart_info_list:
            catalog = info.catalog or 'Others'
            catalog2info[catalog].append(info)
            if info.catalog and info.catalog not in group_names:
                group_names.append(info.catalog)
        grouped_data = []
        for g_name in group_names:
            grouped_data.append(
                (g_name, catalog2info[g_name])
            )
        grouped_data.append(('Others', catalog2info['Others']))
        return grouped_data

    def get_or_none(self, name: str) -> Optional[ChartInfo]:
        for info in self._chart_info_list:
            if info.name == name:
                return info

    def count(self) -> int:
        return len(self._chart_info_list)
