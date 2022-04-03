# coding=utf8

import unittest
from collections import namedtuple
from unittest.mock import patch, MagicMock

from django_echarts.core.settings_store import SettingsStore

MockAppConfig = namedtuple('MockAppConfig', 'name')


class SettingsWithStaticUrlTestCase(unittest.TestCase):
    @patch('django.apps.apps.get_app_configs')
    def test_default_settings(self, get_func):
        get_func.return_value = [MockAppConfig('django_echarts.contrib.bootstrap5')]
        target_store = SettingsStore(
            echarts_settings={
                'dms_repo': 'pyecharts',
                'theme_app': 'django_echarts.contrib.bootstrap5',
                'dep2url': {
                    'foo': 'https://foo.icc/foo.js',
                    'zzz': '#local',
                    'err':'#err'
                }
            },
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )
        self.assertEqual(
            'https://assets.pyecharts.org/assets/echarts.min.js',
            target_store.resolve_url('echarts.min')
        )
        self.assertEqual(
            'https://assets.pyecharts.org/assets/maps/china.js',
            target_store.resolve_url('china.js')
        )
        self.assertEqual('https://fuzzy.io', target_store.resolve_url('https://fuzzy.io'))
        self.assertEqual('https://foo.icc/foo.js', target_store.resolve_url('foo'))
        self.assertEqual('/static/assets/zzz.js', target_store.resolve_url('zzz'))
        with self.assertRaises(ValueError):
            target_store.resolve_url('err')

        theme = target_store.theme
        self.assertEqual(theme.name, 'bootstrap5')
        self.assertEqual(theme.theme_palette, 'bootstrap5')
        self.assertEqual(target_store.theme_manger.table_css(), 'table table-responsive')
        self.assertIn('bootstrap5.cerulean', target_store.theme_manger.available_palettes)
        self.assertTrue(len(list(target_store.dependency_manager.iter_download_resources('echarts', 'pyecharts'))) > 0)

        loc_theme = theme.local_theme()
        self.assertEqual(loc_theme.name, 'bootstrap5')
        self.assertTrue(len(theme.js_urls) > 0)
        self.assertTrue(len(theme.css_urls) > 0)
        self.assertTrue(len(list(theme.iter_local_paths())) > 0)

    @patch('django.apps.apps.get_app_configs')
    def test_palette_theme(self, get_func):
        get_func.return_value = [MockAppConfig('django_echarts.contrib.bootstrap5')]
        target_store = SettingsStore(
            echarts_settings={
                'dms_repo': 'pyecharts',
                'theme_app': 'django_echarts.contrib.bootstrap5',
                'theme_name': 'bootstrap5.yeti'
            },
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )
        theme = target_store.theme
        self.assertEqual('bootstrap5.yeti', theme.theme_palette)

        theme2 = target_store.create_theme('bootstrap5.yeti')
        self.assertEqual('bootstrap5.yeti', theme2.theme_palette)

    @patch('django.apps.apps.get_app_configs')
    def test_uninstalled_app(self, get_func):
        get_func.return_value = []
        with self.assertRaises(ValueError):
            SettingsStore(
                echarts_settings={
                    'dms_repo': 'pyecharts',
                    'theme_app': 'django_echarts.contrib.bootstrap5',
                    'theme_name': 'bootstrap5.yeti'
                },
                extra_settings={
                    'STATIC_URL': '/static/'
                }
            )

    @patch('django.apps.apps.get_app_configs')
    def test_unmatched_app(self, get_func):
        get_func.return_value = [MockAppConfig('django_echarts.contrib.bootstrap5')]
        with self.assertRaises(ValueError):
            SettingsStore(
                echarts_settings={
                    'dms_repo': 'pyecharts',
                    'theme_app': 'django_echarts.contrib.bootstrap5',
                    'theme_name': 'bootstrap3.yeti'
                },
                extra_settings={
                    'STATIC_URL': '/static/'
                }
            )

    @patch('django.apps.apps.get_app_configs')
    def test_without_settings_app(self, get_func):
        get_func.return_value = [MockAppConfig('django_echarts.contrib.bootstrap5')]
        target_store = SettingsStore(
            echarts_settings={
                'dms_repo': 'pyecharts',
                # 'theme_app': 'django_echarts.contrib.bootstrap5',
                'theme_name': 'bootstrap5.yeti'
            },
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )
        theme = target_store.theme
        self.assertEqual('bootstrap5.yeti', theme.theme_palette)
