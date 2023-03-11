"""A extension for geojson."""
import warnings
from collections import namedtuple

from django_echarts.custom_maps import use_custom_map, custom_map_url

__all__ = ['use_geojson', 'geojson_url']

warnings.warn('The django_echarts.geojson is deprecated.Use django_echarts.custom_maps instead.', DeprecationWarning)

GeojsonItem = namedtuple('GeojsonItem', 'map_name url')


def use_geojson(chart_obj, map_name: str, url: str = None):
    """Register and use geojson map for a chart."""
    use_custom_map(chart_obj, map_name, url)


def geojson_url(geojson_name: str) -> str:
    """Get default url for a geojson file."""
    return custom_map_url(geojson_name)
