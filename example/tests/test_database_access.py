# coding=utf8

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from demo import models


class FetchQuerySetTestCase(TestCase):
    def setUp(self):
        for d in range(-30, 0):
            models.TemperatureRecord.objects.create(
                high=15,
                low=12,
                create_time=timezone.now() + timedelta(days=d)
            )

    def test_fetch_with_queryset(self):
        high_values, low_values = models.TemperatureRecord.objects.as_axis_values('high', 'low')
        self.assertEqual(30, len(high_values))
        self.assertTrue(all([x == 15 for x in high_values]))
        self.assertEqual(30, len(low_values))
        self.assertTrue(all([x == 12 for x in low_values]))

    def test_fetch_with_values(self):
        high_values, low_values = models.TemperatureRecord.objects.values('high', 'low').as_axis_values('high', 'low')
        self.assertEqual(30, len(high_values))
        self.assertTrue(all([x == 15 for x in high_values]))
        self.assertEqual(30, len(low_values))
        self.assertTrue(all([x == 12 for x in low_values]))

    def test_fetch_with_values_list(self):
        high_values, low_values = models.TemperatureRecord.objects.values_list(
            'high', 'low', named=True
        ).as_axis_values(
            'high', 'low'
        )
        self.assertEqual(30, len(high_values))
        self.assertTrue(all([x == 15 for x in high_values]))
        self.assertEqual(30, len(low_values))
        self.assertTrue(all([x == 12 for x in low_values]))
