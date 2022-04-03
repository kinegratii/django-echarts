from django_echarts.core.tms import parse_theme_label

import unittest


class ThemeLabelParseTestCase(unittest.TestCase):

    def test_parse_label(self):
        self.assertEqual(parse_theme_label('bootstrap5'), ('bootstrap5', 'bootstrap5', '', False))
        self.assertEqual(parse_theme_label('bootstrap5#local'), ('bootstrap5', 'bootstrap5', '', True))
        self.assertEqual(parse_theme_label('bootstrap5.foo#local'), ('bootstrap5.foo', 'bootstrap5', 'foo', True))
