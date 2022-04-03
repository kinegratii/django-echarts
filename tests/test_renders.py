import os
import unittest

from django import setup
from django_echarts.entities import Title, LinkItem
from django_echarts.renders import render_widget
from pyecharts.charts import Bar


# os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_mock'
# setup(set_prefix=False)


class RenderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_mock'
        setup(set_prefix=False)

    def test_render_chart(self):
        bar = Bar()
        bar.width = 200
        self.assertIn('200px', render_widget(bar))

    def test_basic_render(self):
        self.assertEqual('', render_widget(None))
        tw = Title('DemoTitle')
        self.assertTrue('DemoTitle' in render_widget(tw))
        link = LinkItem('demo', url='https://www.baidu.com', new_page=True)
        html = render_widget(link)
        self.assertIn('target="_blank"', html)
