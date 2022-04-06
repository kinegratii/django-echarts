import os
import unittest
from borax.htmls import HTMLString
from django import setup
from django_echarts.entities import Title, LinkItem, ChartInfo, bootstrap_table_class, material_table_class
from django_echarts.renders import render_widget
from pyecharts.charts import Bar
from pyecharts.components import Table


class TableCssTestCase(unittest.TestCase):
    def test_table_css(self):
        self.assertEqual(
            'table table-responsive table-bordered table-striped table-md',
            bootstrap_table_class(border=True, striped=True, size='md'))
        self.assertEqual(
            'table table-responsive table-borderless table-striped table-md',
            bootstrap_table_class(borderless=True, striped=True, size='md'))
        self.assertEqual('responsive-table striped centered', material_table_class(striped=True, center=True))


class RenderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_mock'
        setup(set_prefix=False)

    def test_settings(self):
        from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
        self.assertEqual('bootstrap5', DJANGO_ECHARTS_SETTINGS.theme.name)

    def test_render_default(self):
        with self.assertRaises(TypeError):
            render_widget(object)
        info = ChartInfo('DemoInfo')
        self.assertIn('DemoInfo', render_widget(info))
        self.assertEqual('xxx', render_widget(HTMLString('xxx')))

    def test_render_chart(self):
        bar = Bar()
        bar.width = 200
        self.assertIn('200px', render_widget(bar))
        table = Table()
        self.assertIn('</div>', render_widget(table))

    def test_basic_render(self):
        self.assertEqual('', render_widget(None))
        tw = Title('DemoTitle')
        self.assertTrue('DemoTitle' in render_widget(tw))
        link = LinkItem('demo', url='https://www.baidu.com', new_page=True)
        html = render_widget(link)
        self.assertIn('target="_blank"', html)


class TemplateTagsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_mock'
        setup(set_prefix=False)
        from django.template import engines
        django_engine = engines['django']
        cls.template_obj = django_engine.from_string('{% load echarts %}{% dw_widget widget %}')

    def test_tags(self):
        tw = Title('DemoTitle')
        result = self.template_obj.render({'widget': tw})
        self.assertIn('DemoTitle', result)
