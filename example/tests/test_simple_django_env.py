# coding=utf8

from django.test import TestCase

from demo import models


class SimpleTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(2, 1 + 1)

    def test_with_django_env(self):
        models.TemperatureRecord.objects.create(
            high=15,
            low=12
        )
        self.assertEqual(1, models.TemperatureRecord.objects.count())
