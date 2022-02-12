from django.template import Context, Template
from django.test import TestCase


class MyTagsTestCase(TestCase):
    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_js_dep(self):
        rendered = self.render_template(
            r'{% load echarts %}{% echarts_js_dependencies "china" %}'
        )
        self.assertIn('https://assets.pyecharts.org/assets/maps/china.js', rendered)
        rendered = self.render_template('{% load echarts %}{% dep_url "china" "pyecharts" %}')
        self.assertEqual('https://assets.pyecharts.org/assets/maps/china.js', rendered)
        rendered = self.render_template('{% load echarts %}{% dep_url "china" %}')
        self.assertEqual('https://assets.pyecharts.org/assets/maps/china.js', rendered)
