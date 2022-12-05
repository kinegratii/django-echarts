import unittest

from django_echarts.entities.base import ChartIdentification


class ChartIdentificationTestCase(unittest.TestCase):
    def test_basic(self):
        ci1 = ChartIdentification('yearly_chart', {'year': 2022})
        self.assertEqual('year/2022/', ci1.generate_url())
