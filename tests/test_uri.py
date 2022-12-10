import unittest
from django_echarts.entities.uri import EntityURI


class EntityURITestCase(unittest.TestCase):
    def test_parse(self):
        mya_uri = EntityURI.from_params_path('chart', 'demo', 'year/2021/tag/hello/django-echarts',
                                             param_names=['year', 'tag'])
        self.assertDictEqual({'year': '2021', 'tag': 'hello/django-echarts'}, mya_uri.params)
        mya_uri2 = EntityURI.from_params_path('chart', 'demo', 'year/2021/tag/hello/django-echarts/',
                                              param_names=['year', 'tag'])
        self.assertDictEqual({'year': '2021', 'tag': 'hello/django-echarts/'}, mya_uri2.params)

    def test_full_str(self):
        my_uri = EntityURI.from_str('chart:name1')
        self.assertEqual('chart', my_uri.catalog)
        self.assertEqual('name1', my_uri.name)
        self.assertEqual(0, len(my_uri.params))

        uri_with_params = EntityURI.from_str('chart:name1/year/2022')
        self.assertEqual('chart', uri_with_params.catalog)
        self.assertEqual('name1', uri_with_params.name)
        self.assertEqual('2022', uri_with_params.params['year'])

    def test_custom_catalog(self):
        uri_with_params = EntityURI.from_str('name1/year/2022', catalog='chart')
        self.assertEqual('chart', uri_with_params.catalog)
        self.assertEqual('name1', uri_with_params.name)
        self.assertEqual('2022', uri_with_params.params['year'])
