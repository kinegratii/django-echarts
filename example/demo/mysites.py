from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
from django_echarts.starter.sites import DJESite, DJESiteDetailView
from .demo_data import FACTORY

site_obj = DJESite(
    site_title='图表可视化',
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts'),
    theme='bootstrap3.cerulean'
)

site_obj.add_widgets(
    Jumbotron('图表可视化', main_text='这是一个由django-echarts-starter驱动的可视化网站。', small_text='版本1.0'),
)
site_obj.add_link(LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True))
site_obj.add_link(LinkItem(text='返回首页', url='/'))


@site_obj.register_chart(description='词云示例', menu_text='示例一')
def my_cloud():
    return FACTORY.create('word_cloud')


@site_obj.register_chart
def mychart():
    return FACTORY.create('kline')


class MyDemoDetailView(DJESiteDetailView):
    charts_config = [('c1', '柱形图'), ('c2', '饼图')]

    def dje_chart_c1(self, *args, **kwargs):
        return FACTORY.create('bar')

    def dje_chart_c2(self, *args, **kwargs):
        return FACTORY.create('pie')


site_obj.register_detail_view(MyDemoDetailView, menu_text='示例一')
