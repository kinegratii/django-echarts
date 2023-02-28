import unittest
from collections import namedtuple
from unittest.mock import patch

from django_echarts.core.settings_store import SettingsStore, DJEOpts

MockAppConfig = namedtuple('MockAppConfig', 'name')


class DMSFromSettingsTestCase(unittest.TestCase):
    @patch('django.apps.apps.get_app_configs')
    def test_custom_url_settings(self, get_func):
        get_func.return_value = [MockAppConfig('django_echarts.contrib.bootstrap5')]
        target_store = SettingsStore(
            echarts_settings=DJEOpts(dms_repo='pyecharts', theme_app='django_echarts.contrib.bootstrap5', dep2url={
                'foo': 'https://foo.icc/foo.js',
                'zzz': '#local',
                'err': '#err',
                '#local': ['c1', 'c2']
            }),
            extra_settings={
                'STATIC_URL': '/static/'
            }
        )

        self.assertEqual('/static/assets/zzz.js', target_store.resolve_url('zzz'))
        self.assertEqual('/static/assets/c1.js', target_store.resolve_url('c1'))
        self.assertEqual('/static/assets/c2.js', target_store.resolve_url('c2'))
