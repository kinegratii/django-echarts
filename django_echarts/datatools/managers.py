# coding=utf8

from borax.datasets.fetch import fetch
from django.db import models


class AxisValuesQuerySet(models.QuerySet):
    def as_axis_values(self, *keys, **kwargs):
        return fetch(self, *keys, **kwargs)
