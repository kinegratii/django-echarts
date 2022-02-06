from django_echarts.starter.sites import DJESite
from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
from .demo_data import FACTORY

site_obj = DJESite(
    site_title='图表可视化',
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts'),
    # theme='bootstrap3.cerulean',
    theme='material'
)

site_obj.add_widgets(
    Jumbotron('图表可视化', main_text='这是一个由django-echarts-starter驱动的可视化网站。', small_text='版本1.0'),
)
site_obj.add_link(LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True))
site_obj.add_link(LinkItem(text='返回首页', url='/'))


@site_obj.register_chart(description='词云示例', menu_text='示例一', top=1)
def my_cloud():
    return FACTORY.create('word_cloud')


@site_obj.register_chart
def my_kline():
    return FACTORY.create('kline')


@site_obj.register_chart(name='c1', title='柱形图', description='福建省各地市面积排行', menu_text='分组1')
def my_bar():
    return FACTORY.create('bar')


@site_obj.register_chart(name='c2', title='饼图示例', description='车站收入分布图', menu_text='分组1')
def my_pie():
    return FACTORY.create('pie')
