# coding=utf8
"""
A interface module for pyecharts.
In the practice, pyecharts should not be explicitly imported.
"""

from datetime import datetime, date, time
import json
from functools import singledispatch


# ---------- Adapter for Chart Attributes ----------

def to_css_length(l):
    if isinstance(l, (int, float)):
        return '{}px'.format(l)
    else:
        return l


def merge_js_dependencies(*chart_or_name_list):
    front_must_items = ['echarts']
    front_optional_items = ['echartsgl']
    dependencies = []
    fist_items = set()

    def _add(_item):
        if _item in front_must_items:
            pass
        elif _item in front_optional_items:
            fist_items.add(_item)
        elif _item not in dependencies:
            dependencies.append(_item)

    for d in chart_or_name_list:
        if hasattr(d, 'js_dependencies'):
            for x in d.js_dependencies:
                _add(x)
        elif isinstance(d, (list, tuple, set)):
            for x in d:
                _add(x)
        elif isinstance(d, str):
            _add(d)
    return front_must_items + [x for x in front_optional_items if x in fist_items] + dependencies


# ---------- Javascript Dump Tools ----------
@singledispatch
def json_encoder(obj):
    raise TypeError(repr(obj) + " is not JSON serializable")


@json_encoder.register(datetime)
@json_encoder.register(date)
@json_encoder.register(time)
def encode_date_time(obj):
    return obj.isoformat()


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
