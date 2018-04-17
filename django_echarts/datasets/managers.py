# coding=utf8

from django.db import models
from borax.fetch import fetch


class AxisValuesQuerySet(models.QuerySet):
    def as_axis_values(self, *keys, **kwargs):
        return fetch(self, *keys, **kwargs)
