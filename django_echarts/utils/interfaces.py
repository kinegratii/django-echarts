# coding=utf8
"""
A interface module for pyecharts.
"""
import json
from datetime import datetime, date, time
from functools import singledispatch

from pyecharts.charts.base import default as json_encode_func
from pyecharts.commons.utils import OrderedSet

__all__ = ['to_css_length', 'merge_js_dependencies', 'JsDumper']


# ---------- Adapter for Chart Attributes ----------

def to_css_length(val):
    """
    Return the standard length string of css.
    It's compatible with number values in old versions.
    :param val: source css length.
    :return: A string.
    """
    if isinstance(val, (int, float)):
        return '{}px'.format(val)
    else:
        return val


def _flat(ele):
    if hasattr(ele, 'js_dependencies'):
        if isinstance(ele.js_dependencies, list):
            return ele.js_dependencies
        if hasattr(ele.js_dependencies, 'items'):
            return list(ele.js_dependencies.items)  # pyecharts.commons.utils.OrderedSet
        raise ValueError('Can not parse js_dependencies.')
    if isinstance(ele, (list, tuple, set)):
        return ele
    return ele,


def merge_js_dependencies(*chart_or_name_list):
    front_required_items = ['echarts']
    front_optional_items = ['echartsgl']
    dependencies = []
    fist_items = set()

    def _add(_item):
        if _item in front_required_items:
            pass
        elif _item in front_optional_items:
            fist_items.add(_item)
        elif _item not in dependencies:
            dependencies.append(_item)

    for d in chart_or_name_list:
        for _d in _flat(d):
            _add(_d)
    return front_required_items + [x for x in front_optional_items if x in fist_items] + dependencies


# ---------- Javascript Dump Tools ----------
@singledispatch
def json_encoder(obj):
    return json_encode_func(obj)


@json_encoder.register(datetime)
@json_encoder.register(date)
@json_encoder.register(time)
def encode_date_time(obj):
    return obj.isoformat()


@json_encoder.register(OrderedSet)
def encode_js_dependency(obj):
    return obj.items


class JsDumper:
    @staticmethod
    def as_object(data):
        """
        Dump object to multiple-line javascript object.
        :param data:
        :return:
        """
        return json.dumps(data, indent=4, default=json_encoder)

    @staticmethod
    def as_parameters(*parameters, variables=None):
        """
        Dump python list as the parameter of javascript function
        :param parameters:
        :param variables:
        :return:
        """
        s = json.dumps(parameters)
        s = s[1:-1]
        if variables:
            for v in variables:
                if v in parameters:
                    s = s.replace('"' + v + '"', v)
        return s
