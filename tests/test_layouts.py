import unittest

from django_echarts.entities import RowContainer, HTMLBase
from django_echarts.entities.layouts import any2layout


class MockWidget(HTMLBase):
    pass


class LayoutOptsTestCase(unittest.TestCase):
    def test_create_layout_opts(self):
        lto = any2layout('l8')
        self.assertEqual('l', lto.pos)
        self.assertListEqual([8], lto.spans)
        self.assertEqual(False, lto.start)

        with self.assertRaises(ValueError):
            any2layout('e4')

        lto2 = any2layout(9)
        self.assertListEqual([9], lto2.spans)

        lto3 = any2layout([4, 8])
        self.assertListEqual([4, 8], lto3.spans)

        s_lto3 = lto.stripped_layout()
        self.assertEqual('r', s_lto3.pos)
        self.assertListEqual([8], s_lto3.spans)


class RowContainerTestCase(unittest.TestCase):
    def test_row_container_layout(self):
        rc = RowContainer()
        rc.add_widget(MockWidget(), span=2)
        rc.add_widget(MockWidget(), span=10)
        rc.auto_layout()
        self.assertTupleEqual((2, 10), rc.get_spans())

        rc2 = RowContainer()
        rc2.add_widget(MockWidget(), span=2)
        rc2.add_widget(MockWidget())
        rc2.auto_layout()
        self.assertTupleEqual((2, 10), rc.get_spans())

    def test_set_spans(self):
        rc = RowContainer()
        rc.add_widget(MockWidget(), span=2)
        rc.add_widget(MockWidget(), span=10)
        rc.set_spans([4, 8])
        self.assertTupleEqual((4, 8), rc.get_spans())
        rc.set_spans(6)
        self.assertTupleEqual((6, 6), rc.get_spans())


