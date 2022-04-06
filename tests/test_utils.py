import unittest
from django_echarts.utils.burl import burl_kwargs, burl_args, BUrl
from django_echarts.utils.lazy_dict import LazyDict


class BurlTestCase(unittest.TestCase):
    def test_burl(self):
        self.assertEqual(
            '/foo/?p=1&q=test',
            burl_args('/foo/', 'p', 1, 'q', 'test')
        )
        self.assertEqual('/foo/?p=1&q=test', burl_kwargs('/foo/', p=1, q='test'))
        self.assertEqual('/foo/?p=1&q=test', burl_kwargs('/foo/?p=1', q='test'))
        url = BUrl('/foo/')
        url.append('p', 1)
        url.append('z', 'zoo')
        url.delete('z')
        self.assertEqual('/foo/?p=1', url.url)


class LazyDictTestCase(unittest.TestCase):
    def test_lazy_dict(self):
        l_dic = LazyDict()
        l_dic.register('value1', 'key1')
        l_dic.set_ref('ref1', 'key1')

        self.assertEqual(1, len(l_dic))
        self.assertTrue('key1' in l_dic)
        self.assertTrue('value1' == l_dic.get('key1') == l_dic.get('ref1'))
        self.assertTrue('key1' == l_dic.actual_key('key1') == l_dic.actual_key('ref1'))

        with self.assertRaises(TypeError):
            l_dic.register('error1')

        @l_dic.inject('key1')
        def demo(key1):
            return key1

        self.assertEqual('value1', demo())
