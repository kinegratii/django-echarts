import unittest

from django_echarts.entities import Nav, Menu, LinkItem


class NavTestCase(unittest.TestCase):
    def test_nav(self):
        nav = Nav()
        nav.add_menu('Menu1', slug='menu1', url='/menu1')
        nav.add_item('Menu1', LinkItem('sub1', '/sub/', after_separator=True))

        self.assertEqual(1, len(nav.menus))
        self.assertEqual('sub1', nav.menus[0].children[0].text)
        self.assertEqual(True, nav.menus[0].children[0].after_separator)
