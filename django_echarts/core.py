# coding=utf8

from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic.base import View


class EchartsBaseMixin(object):
    option = {}

    def get_echarts_option(self, **kwargs):
        return self.option


class EchartsView(EchartsBaseMixin, View):
    def get(self, request, **kwargs):
        echarts_option = self.get_echarts_option(**kwargs)
        return JsonResponse(data=echarts_option, safe=False)
