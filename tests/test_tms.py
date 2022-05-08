from django_echarts.core.tms import parse_theme_label, ThemeManager

import unittest


class ThemeLabelParseTestCase(unittest.TestCase):

    def test_parse_label(self):
        self.assertEqual(parse_theme_label('bootstrap5'), ('bootstrap5', 'bootstrap5', '', False))
        self.assertEqual(parse_theme_label('bootstrap5#local'), ('bootstrap5', 'bootstrap5', '', True))
        self.assertEqual(parse_theme_label('bootstrap5.foo#local'), ('bootstrap5.foo', 'bootstrap5', 'foo', True))


class ThemeWithCustomUrlTestCase(unittest.TestCase):
    def test_custom_url(self):
        manager = ThemeManager.create_from_module('django_echarts.contrib.bootstrap3', d2u={
            'bootstrap3': {'main_css': '/my/bootstrap3.min.css'},
            'bootstrap3.foo': {'palette_css': '/my/bootstrap3.foo.min.css'}
        })

        theme1 = manager.create_theme('bootstrap3')
        css_urls = theme1.css_urls
        self.assertIn('/my/bootstrap3.min.css', css_urls)

        theme2 = manager.create_theme('bootstrap3.foo')
        css_urls2 = theme2.css_urls
        self.assertIn('/my/bootstrap3.foo.min.css', css_urls2)

    def test_incorrect_usage(self):
        manager = ThemeManager.create_from_module('django_echarts.contrib.bootstrap3', d2u={
            'bootstrap3': {'palette_css': '/my/bootstrap3.min.css'},
            'bootstrap3.foo': {'main_css': '/my/bootstrap3.foo.min.css'}
        })

        theme1 = manager.create_theme('bootstrap3')
        css_urls = theme1.css_urls
        self.assertNotIn('/my/bootstrap3.min.css', css_urls)

        theme2 = manager.create_theme('bootstrap3.foo')
        css_urls2 = theme2.css_urls
        self.assertNotIn('/my/bootstrap3.foo.min.css', css_urls2)


class ThemeLocalTestCase(unittest.TestCase):
    def test_local_theme(self):
        pass
