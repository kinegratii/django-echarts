import json
import os
from dataclasses import dataclass

from django.contrib.staticfiles import finders
from django.http.response import JsonResponse, HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy, path
from django.views.generic.base import View

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS

__all__ = ['use_custom_map', 'custom_map_url', 'custom_map_urlpatterns']


@dataclass
class CustomMapItem:
    """A map data structure for geojson & svg map."""
    map_name: str
    url: str
    catalog: str
    param_str: str  # param string in echarts.registerMap
    ajax_data_type: str

    def __eq__(self, other):
        return isinstance(other, CustomMapItem) and self.map_name == other.map_name

    def __hash__(self):
        return hash(self.map_name)


def create_custom_map_item(map_name: str, url: str, echarts_version: str):
    if any([
        url.endswith('.geojson'), url.endswith('.json'), url.endswith('svg'),
        map_name.endswith('.geojson'), map_name.endswith('.json'), map_name.endswith('.svg')
    ]):
        catalog = url.split('.')[-1]
        if catalog == 'json':
            catalog = 'geojson'
        if echarts_version[0] == '4':
            if catalog == 'geojson':
                param_str = 'mapData'
                ajax_data_type = 'json'
            else:
                raise ValueError('The svg map is unsupported for echarts 4.')
        else:
            if catalog == 'geojson':
                param_str = '{geoJSON:mapData}'
                ajax_data_type = 'json'
            else:
                param_str = '{svg:mapData}'
                ajax_data_type = 'text'
        return CustomMapItem(map_name=map_name, url=url, catalog=catalog, param_str=param_str,
                             ajax_data_type=ajax_data_type)
    else:
        raise ValueError('Unsupported custom map catalogs.')


def use_custom_map(chart_obj, map_name: str, url_or_filename: str = None):
    """Register and use geojson & svg map for a chart."""
    echarts_version = DJANGO_ECHARTS_SETTINGS.opts.echarts_version
    url_or_filename = url_or_filename or map_name
    if not any([
        url_or_filename.startswith('https://'),
        url_or_filename.startswith('http://'),
        url_or_filename.startswith('/')
    ]):
        map_data_url = reverse_lazy(_VIEW_NAME, args=(url_or_filename,))
    else:
        map_data_url = url_or_filename
    # TODO Check chart.maptype and map_name ?
    # Map.options['series'][i]['mapType']  Geo.options['geo']['map']
    setattr(chart_obj, 'custom_map_item', create_custom_map_item(map_name, map_data_url, echarts_version))


_VIEW_NAME = 'dje_map_data'


def custom_map_url(map_name: str) -> str:
    """Get default url for a custom file."""
    return reverse_lazy(_VIEW_NAME, args=(map_name,))


def _get_custom_map_file_path(map_name: str) -> str:
    # ctomstr
    finder_param_path = [f'assets/custom_maps/{map_name}']
    if map_name.endswith('.geojson') or map_name.endswith('.json'):  # Compatible with old geojson(0.5.x)
        finder_param_path.append(f'geojson/{map_name}')
    for fpp in finder_param_path:
        result = finders.find(fpp, all=False)
        if result:
            return result


class CustomMapDataView(View):
    def get(self, request, *args, **kwargs):
        map_name = self.kwargs.get('map_name')
        file_path = _get_custom_map_file_path(map_name)
        if not file_path or not os.path.exists(file_path):
            return HttpResponseNotFound('The map file does not exist.')
        if file_path.endswith('.geojson') or file_path.endswith('.json'):
            return self.return_geojson_map_rsp(file_path)
        elif file_path.endswith('.svg'):
            return self.return_svg_map_rsp(file_path)
        else:
            return HttpResponseNotFound('Unsupported map type. geojson or svg is required.')

    def return_geojson_map_rsp(self, file_path):
        with open(file_path, 'r', encoding='utf8') as fp:
            data = json.load(fp)
        return JsonResponse(data, safe=False)

    def return_svg_map_rsp(self, file_path):
        with open(file_path, 'r', encoding='utf8') as fp:
            content = fp.read()
        rsp = HttpResponse(content_type='text/plain')
        rsp.write(content)
        return rsp


custom_map_urlpatterns = [
    path('map_data/<str:map_name>', CustomMapDataView.as_view(), name=_VIEW_NAME)
]
