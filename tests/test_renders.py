import os
import unittest
from borax.htmls import HTMLString
from django import setup
from django_echarts.entities import (
    Title, LinkItem, ChartInfo, bootstrap_table_class, material_table_class, Message, ValueItem, RowContainer
)
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

    def test_render_container(self):
        rc = RowContainer()
        rc.add_widget(ValueItem(45, 'Today Value'))
        rc.add_widget(Message('xxF'))
        rc.set_spans(6)
        self.assertTupleEqual((6, 6), rc.get_spans())


class TemplateTagsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_mock'
        setup(set_prefix=False)
        from django.template import engines
        cls.django_engine = engines['django']

    def test_tags(self):
        tw = Title('DemoTitle')
        template_obj = self.django_engine.from_string('{% load echarts %}{% dw_widget widget %}')
        result = template_obj.render({'widget': tw})
        self.assertIn('DemoTitle', result)

    def test_theme(self):
        template_obj = self.django_engine.from_string('{% load echarts %}{% theme_js %} {% theme_css %}')
        result = template_obj.render()
        self.assertIn('link', result)
        self.assertIn('script', result)

    def test_init_echarts(self):
        bar = Bar()
        template_obj = self.django_engine.from_string(' '.join([
            '{% load echarts %}{% echarts_js_content widget %}',
            '{% echarts_container widget %}',
            '{% echarts_js_dependencies widget %}'
        ]))
        result = template_obj.render({'widget': bar})
        self.assertIn('getElementById', result)
        self.assertIn('echarts.min.js', result)

        template_obj2 = self.django_engine.from_string('{% load echarts %}{% echarts_js_content_wrap widget %}')
        result2 = template_obj2.render({'widget': bar})
        self.assertIn('getElementById', result2)
