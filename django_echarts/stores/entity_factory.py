from typing import Type, Tuple, Optional, Any, Union

from django_echarts.entities import (WidgetGetterMixin, ChartInfoManagerMixin, LocalChartInfoManager, ChartInfo,
                                     EntityURI)
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
    def html_widget_manger(self) -> LazyDict:
        return self._html_widgets

    @property
    def chart_manager(self) -> LazyDict:
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
                if self._chart_obj_dic.has_parameters(cname):
                    c_info.set_bound(False)
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

    def get_chart_and_info(self, name: str, params: dict = None) -> Tuple[Optional[Any], bool, Optional[ChartInfo]]:
        """Execute chart creator and return pyecharts chart object.
        Use get_chart_widget instead if the info is not used.
        """
        if name in self._chart_obj_dic:
            params = params or {}
            func_exists = True
            chart_obj = self._chart_obj_dic.get(name, params)
            info_name = self._chart_obj_dic.actual_key(name)
            info = self._chart_info_manager.get_or_none(info_name)
            return chart_obj, func_exists, info
        else:
            return None, False, None

    def get_chart_widget(self, name: str, params: dict = None) -> Any:
        return self._chart_obj_dic.get(name, params)

    def get_html_widget(self, name: str, params: dict = None) -> Any:
        return self._html_widgets.get(name, params)

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

    # Methods related Entity URI

    def clean_uri_params(self, uri: EntityURI) -> bool:
        """Validate and convert params inplace.And return parametric flag for the name"""
        if uri.catalog in ('chart', 'info'):
            uri.params, is_parametric = self.chart_manager.validate_caller_params(uri.name, uri.params)
        else:
            uri.params, is_parametric = self.html_widget_manger.validate_caller_params(uri.name, uri.params)
        return is_parametric

    def get_widget_by_uri(self, uri: EntityURI):
        if uri.is_empty():
            return None
        self.clean_uri_params(uri)
        if uri.catalog == 'chart':
            return self._chart_obj_dic.get(uri.name, uri.params)
        elif uri.catalog == 'info':
            # info_name = self._chart_obj_dic.actual_key(uri.name)
            return self._chart_info_manager.get_or_none(uri=uri)
        else:
            return self._html_widgets.get(uri.name, uri.params)

    def get_chart_and_info_by_uri(self, uri: EntityURI):
        if not uri.is_empty() and uri.name in self._chart_obj_dic:
            self.clean_uri_params(uri)
            func_exists = True
            chart_obj = self._chart_obj_dic.get(uri.name, uri.params)
            # info_name = self._chart_obj_dic.actual_key(uri.name)
            info = self._chart_info_manager.get_or_none(uri=uri)
            return chart_obj, func_exists, info
        else:
            return None, False, None

    def get_all_chart_uri(self):
        info_dic = {info.name: info for info in self._chart_info_manager.query_all_chart_info()}
        for chart_name in self._chart_obj_dic.keys():
            if self._chart_obj_dic.has_parameters(chart_name):
                info = info_dic.get(chart_name)
                if info is not None:
                    for params_dic in info.params_config:
                        uri = EntityURI('chart', chart_name, params=params_dic)
                        yield uri
                else:
                    # param functions without provided ParamsConfig.
                    pass
            else:
                uri = EntityURI('chart', chart_name)
                yield uri


# Project entry for entities
factory = EntityFactory()
