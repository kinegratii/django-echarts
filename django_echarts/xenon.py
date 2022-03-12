"""
A integration module with django database.
"""

from typing import List

from django.db import models
from django_echarts.entities import ChartInfoManagerMixin, ChartInfo


class XChartInfo(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    body = models.TextField(max_length=5000)
    catalog = models.CharField(max_length=50)
    top = models.IntegerField(default=0)
    tags = models.JSONField()

    class Meta:
        abstract = True


def chart2model(info: ChartInfo) -> XChartInfo:
    pass


def model2chart(obj: XChartInfo) -> ChartInfo:
    pass


class ChartModelManager(ChartInfoManagerMixin, models.Manager):
    def add_chart_info(self, info: ChartInfo):
        obj = chart2model(info)
        self.create(obj)

    def query_chart_info_list(self, keyword: str = None, with_top: bool = False) -> List[ChartInfo]:
        pass

# Site from database.
