import unittest

from django_echarts.entities import (Title, ChartInfo, WidgetCollection)
from django_echarts.entities.uri import EntityURI, ParamsConfig
from django_echarts.stores.entity_factory import EntityFactory


class MockChart:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class EntityFactoryTestCase(unittest.TestCase):
    def test_factory(self):
        my_factory = EntityFactory()
        my_factory.register_html_widget(Title('Demo1'), name='demo1')
        self.assertEqual('Demo1', my_factory.get_widget_by_name('demo1').text)
        self.assertEqual('Demo1', my_factory.get_html_widget('demo1').text)
        my_factory.register_chart_widget(MockChart('100%', '500px'), name='chart1')
        info = my_factory.get_widget_by_name('info:chart1')
        self.assertTrue(isinstance(info, ChartInfo))
        self.assertEqual('100%', my_factory.get_widget_by_name('chart1').width)
        self.assertEqual('100%', my_factory.get_chart_widget('chart1').width)
        self.assertEqual(1, my_factory.get_chart_total())
        self.assertEqual(None, my_factory.get_widget_by_name('error'))

        chart1, exits, info1 = my_factory.get_chart_and_info('chart1')
        self.assertTrue(isinstance(info1, ChartInfo))

        my_factory.register_chart_widget(MockChart('100%', '400px'), name='chart2', info=False)
        self.assertEqual(None, my_factory.get_widget_by_name('info:chart2'))

        _, exits2, _ = my_factory.get_chart_and_info('chart3')
        self.assertEqual(False, exits2)

        wc = WidgetCollection('test')
        wc.add_chart_widget('chart1')
        wc.add_html_widget(['demo1'])
        wc.auto_mount(my_factory)

    def test_factory_uri_methods(self):
        factory2 = EntityFactory()

        @factory2.register_chart_widget
        def chart1():
            pass

        @factory2.register_chart_widget(info=ChartInfo('chart2'))
        def chart2(year: int):
            pass

        @factory2.register_chart_widget(info=ChartInfo('chart3', params_config=ParamsConfig({'year': [2022, 2023]})))
        def chart3(year: int):
            pass

        uri_list = list(factory2.get_all_chart_uri())
        uri_string_list = [str(uri) for uri in uri_list]
        self.assertEqual(3, len(uri_list))
        self.assertIn('chart:chart3/year/2022', uri_string_list)
        self.assertFalse(any(['chart2' in s for s in uri_string_list]))
