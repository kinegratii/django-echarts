import json
import os
from collections import namedtuple

from django.http.response import JsonResponse, HttpResponseNotFound
from django.urls import reverse_lazy, path
from django.views.generic.base import View

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS

__all__ = ['use_geojson', 'geojson_url', 'GeojsonDataView', 'geo_urlpatterns']

GeojsonItem = namedtuple('GeojsonItem', 'map_name url')

_VIEW_NAME = 'dje_geojson'


def use_geojson(chart_obj, map_name: str, url: str = None):
    """Register and use geojson map for a chart."""
    setattr(chart_obj, 'geojson', GeojsonItem(map_name, url))


def geojson_url(geojson_name: str) -> str:
    """Get default url for a geojson file."""
    return reverse_lazy(_VIEW_NAME, args=(geojson_name,))


class GeojsonDataView(View):
    def get(self, request, *args, **kwargs):
        geojson_name = self.kwargs.get('geojson_name')
        file_path = DJANGO_ECHARTS_SETTINGS.get_geojson_path(geojson_name)
        if not os.path.exists(file_path):
            return HttpResponseNotFound('The geojson file does not exist.')
        with open(file_path, 'r', encoding='utf8') as fp:
            data = json.load(fp)
        return JsonResponse(data, safe=False)


geo_urlpatterns = [
    path('geojson/<str:geojson_name>', GeojsonDataView.as_view(), name=_VIEW_NAME)
]
