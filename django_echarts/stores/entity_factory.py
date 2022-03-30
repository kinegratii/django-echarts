from typing import Type, Tuple, Optional, Any, Union

from django_echarts.entities import WidgetGetterMixin, ChartInfoManagerMixin, LocalChartInfoManager, ChartInfo
from django_echarts.utils.lazy_dict import LazyDict


class EntityFactory(WidgetGetterMixin):
    """A entity store."""
    chart_info_manager_class = LocalChartInfoManager  # type: Type[ChartInfoManagerMixin]

    def __init__(self):
        self._html_widgets = LazyDict()  # html_widgets
        self._chart_obj_dic = LazyDict()  # chart_widgets
        self._chart_info_manager = self.chart_info_manager_class()  # type: ChartInfoManagerMixin

    @property
    def html_widgets(self) -> LazyDict:
        return self._html_widgets

    @property
    def chart_widgets(self) -> LazyDict:
        return self._chart_obj_dic

    @property
    def chart_info_manager(self) -> ChartInfoManagerMixin:
        return self._chart_info_manager

    def register_chart_widget(self, function=None, name: str = None, info: Union[bool, ChartInfo] = True):
        def decorator(func):
            cname = name or func.__name__
            self._chart_obj_dic.func_register(func, cname)
            if info is True:
                c_info = ChartInfo(name=cname)
            elif info is False:
                c_info = None
            else:
                c_info = info
            if c_info:
                self.register_chart_info(c_info)
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def register_html_widget(self, function=None, name: str = None):
        def decorator(func):
            self._html_widgets.func_register(func, name)
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def register_chart_info(self, info: ChartInfo):
        self._chart_info_manager.add_chart_info(info)

    def set_chart_ref(self, ref_name: str, name: str):
        self._chart_obj_dic.set_ref(ref_name, name)

    def set_html_ref(self, ref_name: str, name: str):
        self._html_widgets.set_ref(ref_name, name)

    def get_chart_and_info(self, name: str) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Execute chart creator and return pyecharts chart object.
        Use get_chart_widget instead if the info is not used.
        """
        if name in self._chart_obj_dic:
            func_exists = True
            chart_obj = self._chart_obj_dic.get(name)
            info_name = self._chart_obj_dic.actual_key(name)
            info = self._chart_info_manager.get_or_none(info_name)
            return chart_obj, func_exists, info
        else:
            return None, False, None

    def get_chart_widget(self, name: str) -> Any:
        return self._chart_obj_dic.get(name)

    def get_html_widget(self, name: str) -> Any:
        return self._html_widgets.get(name)

    def get_widget_by_name(self, name: str) -> Any:
        if name[:5] == 'info:':
            info_name = self._chart_obj_dic.actual_key(name[5:])
            return self._chart_info_manager.get_or_none(info_name)
        else:
            if name in self._chart_obj_dic:
                return self._chart_obj_dic.get(name)
            elif name in self._html_widgets:
                return self._html_widgets.get(name)
            else:
                return None

    def get_chart_total(self) -> int:
        return len(self._chart_obj_dic)


factory = EntityFactory()
