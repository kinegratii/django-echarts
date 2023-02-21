from django.urls import reverse_lazy
from django_echarts.entities.uri import EntityURI
from typing import Union


def reverse_chart_url(uri_or_name: Union[EntityURI, str], params_dic: dict = None):
    """
    reverse url of a single chart view in DJESite.
    The following three signatures are supported.

    reverse_chart_url(uri:EntityURI)
    reverse_chart_url(name:str)
    reverse_chart_url(name:str, params_dic:dict)
    """
    if isinstance(uri_or_name, EntityURI):
        uri = uri_or_name
    else:
        uri = EntityURI('chart', uri_or_name, params_dic)
    if len(uri.params):
        return reverse_lazy('dje_chart_single', args=(uri.name, uri.params_path))
    else:
        return reverse_lazy('dje_chart_single', args=(uri.name,))
