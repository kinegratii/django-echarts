from django_echarts.starter.sites import DJESite, SiteOpts
from django_echarts.starter.widgets import Jumbotron, Copyright, LinkItem
from .demo_data import FACTORY

site_obj = DJESite(
    site_title='图表可视化',
    # theme='bootstrap3.cerulean',
    theme='bootstrap5',
    # theme='material',
    opts=SiteOpts(
        list_layout='grid',
        # paginate_by=1
    )
)

site_obj.add_widgets(
    jumbotron=Jumbotron('图表可视化', main_text='这是一个由django-echarts-starter驱动的可视化网站。', small_text='版本1.0'),
    copyright_=Copyright(start_year=2017, powered_by='Django-Echarts'),
)
site_obj.add_link(LinkItem(text='Github仓库', url='https://github.com/kinegratii/django-echarts', new_page=True))
site_obj.add_link(LinkItem(text='返回首页', url='/'))


@site_obj.register_chart(description='词云示例', catalog='图表示例', top=1)
def my_cloud():
    return FACTORY.create('word_cloud')


@site_obj.register_chart(title='中国历年冬奥会奖牌榜', description='中国历年冬奥会奖牌榜')
def line_demo():
    return FACTORY.create('line')


@site_obj.register_chart(name='c1', title='福建省各地市面积', description='福建省各地市面积排行', catalog='福建统计', tags=['年度'], top=True)
def my_bar():
    return FACTORY.create('bar')


@site_obj.register_chart(name='c2', title='饼图示例', description='车站收入分布图', catalog='图表示例', tags=['饼图', '收入'])
def my_pie():
    return FACTORY.create('pie')


@site_obj.register_chart(title='3D地图', description='山东省迁移地图', catalog='图表示例')
def map_3d():
    return FACTORY.create('map_3d')


@site_obj.register_chart(name='fj_family_types', title='福建历年家庭结构组成', description='一人户到十人户各占比例', catalog='福建统计')
def fj_family_types():
    return FACTORY.create('timeline_bar')
