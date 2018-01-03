# coding=utf8
"""
A interface module for pyecharts.
In the practice, pyecharts should not be explicitly imported.
"""

from __future__ import unicode_literals

from datetime import datetime, date
import json


class DefaultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        else:
            # Pandas and Numpy lists
            try:
                return obj.astype(float).tolist()
            except Exception:
                try:
                    return obj.astype(str).tolist()
                except Exception:
                    return json.JSONEncoder.default(self, obj)


def dump_options_json(data, indent=0):
    return json.dumps(data, indent=indent, cls=DefaultEncoder)
