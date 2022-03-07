"""
A integration module with models admin
"""

from django.db import models
from django_echarts.entities import ChartInfoManagerMixin, ChartInfo
from django_echarts.starter.sites import DJESite

from typing import List


class MChartInfo(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    body = models.TextField(max_length=5000)
    catalog = models.CharField(max_length=50)
    top = models.IntegerField(default=0)
    tags = models.JSONField()

    class Meta:
        abstract = True


def chart2model(info: ChartInfo) -> MChartInfo:
    pass


def model2chart(obj: MChartInfo) -> ChartInfo:
    pass


class ChartModelManager(ChartInfoManagerMixin, models.Manager):
    def add_chart_info(self, info: ChartInfo):
        obj = chart2model(info)
        self.create(obj)

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[ChartInfo]:
        pass


class ZincSite(DJESite):
    pass
