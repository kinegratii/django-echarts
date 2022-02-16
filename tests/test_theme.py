import unittest

from django_echarts.core.themes import get_theme


class ThemeTestCase(unittest.TestCase):
    def test_bootstrap(self):
        theme = get_theme('bootstrap3.cerulean')
        self.assertIn('https://bootswatch.com/3/cerulean/bootstrap.min.css', theme.css_urls)
        theme2 = get_theme('bootstrap5.yeti')
        self.assertIn('https://bootswatch.com/5/yeti/bootstrap.min.css', theme2.css_urls)
