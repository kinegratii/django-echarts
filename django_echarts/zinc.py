"""
A integration module with models admin
"""

from django.db import models

from django_echarts.starter.sites import DJESite
from django_echarts.core.charttools import ChartManagerMixin


class MChartInfo(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=100)

    class Meta:
        abstract = True


class ChartModelManager(ChartManagerMixin):
    pass


class ZincSite(DJESite):
    pass
