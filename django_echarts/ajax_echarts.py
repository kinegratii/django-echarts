import json
from typing import Any

from django.http.response import JsonResponse
from django.views.generic.base import View
from django_echarts.stores.entity_factory import factory


class ChartOptionsView(View):
    def get(self, request, *args, **kwargs) -> Any:
        chart_name = self.kwargs.get('name')
        chart_obj = factory.get_chart_widget(chart_name)
        if not chart_obj:
            data = {}
        else:
            data = json.loads(chart_obj.dump_options_with_quotes())
        return JsonResponse(data, safe=False)
