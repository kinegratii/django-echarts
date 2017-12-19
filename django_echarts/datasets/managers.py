from __future__ import unicode_literals

from django.db import models
from .fetch import fetch


class FieldValuesQuerySet(models.QuerySet):
    def fetch_values(self, *keys, **kwargs):
        return fetch(self, *keys, **kwargs)
