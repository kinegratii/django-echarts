# coding=utf8


from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Map, Pie, WordCloud, Timeline, Map3D
from pyecharts.globals import ChartType,ThemeType


class ChartFactory:
    def __init__(self):
        self._func = {}
        self._charts = {}

    def collect(self, name):
        def _inject(func):
            self._func[name] = func
            return func

        return _inject

    def create(self, name):
        if name in self._func:
            chart = self._func[name]()
            return chart
        else:
            raise ValueError('No Chart builder for {}'.format(name))


FACTORY = ChartFactory()


@FACTORY.collect('bar')
def create_simple_bar():
    bar = Bar().add_xaxis(["南平", "三明", "龙岩", "宁德", "漳州", "福州", "泉州", "莆田", "厦门"]).add_yaxis(
        '面积', [26300, 22900, 19050, 13450, 12600, 12150, 11020, 4119, 1576]
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="福建省各地市面积排行", subtitle="单位：平方公里"))
    bar.renderer = 'svg'
    return bar


@FACTORY.collect('line')
def create_line():
    data = [
        ['1992年\n阿尔贝维尔', 0, 3, 0], ['1994年\n利勒哈默', 0, 1, 2], ['1998年\n长野', 0, 6, 2], ['2002年\n盐湖城', 2, 2, 4],
        ['2006年\n都灵', 2, 4, 5], ['2010年\n温哥华', 5, 2, 4], ['2014年\n索契', 3, 4, 2], ['2018年\n平昌', 1, 6, 2],
    ]
    years, gnums, snums, cnums = [], [], [], []
    for item in data:
        years.append(item[0])
        gnums.append(item[1])
        snums.append(item[2])
        cnums.append(item[3])
    line = Line().add_xaxis(years).add_yaxis(
        '金牌', gnums).add_yaxis('银牌', snums).add_yaxis('铜牌', cnums).set_global_opts(
        title_opts=opts.TitleOpts(title="中国历年冬奥会奖牌榜"))
    return line


@FACTORY.collect('map')
def create_simple_map():
    data = [('广东', 12601), ('山东', 10152), ('河南', 9936), ('江苏', 8474), ('四川', 8367),
            ('河北', 7461), ('湖南', 6644), ('浙江', 6456), ('安徽', 6102), ('湖北', 5775)]
    max_v = int(max([v[1] for v in data]) * 1.1)
    map1 = (
        Map()
            .add("人口", data, "china")
            .set_global_opts(title_opts=opts.TitleOpts(title="全国第七次人口普查(前10名)", subtitle='单位：万人'),
                             visualmap_opts=opts.VisualMapOpts(is_show=True, max_=max_v))
    )
    map1.renderer = 'svg'
    return map1


@FACTORY.collect('pie')
def create_simple_pie():
    data = [('政府补贴', 389520), ('商业收入', 311040), ('票务收入', 733159)]
    pie = (
        Pie()
            .add("车站收入", data)
            .set_global_opts(title_opts=opts.TitleOpts(title="车站收入结构图", subtitle='单元：元/日'))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return pie


@FACTORY.collect('word_cloud')
def create_word_cloud():
    data = [
        ("生活资源", "999"),
        ("供热管理", "888"),
        ("供气质量", "777"),
        ("生活用水管理", "688"),
        ("一次供水问题", "588"),
        ("交通运输", "516"),
        ("城市交通", "515"),
        ("环境保护", "483"),
        ("房地产管理", "462"),
        ("城乡建设", "449"),
        ("社会保障与福利", "429"),
        ("社会保障", "407"),
        ("文体与教育管理", "406"),
        ("公共安全", "406"),
        ("公交运输管理", "386"),
        ("出租车运营管理", "385"),
        ("供热管理", "375"),
        ("市容环卫", "355"),
        ("自然资源管理", "355"),
        ("粉尘污染", "335"),
        ("噪声污染", "324"),
        ("土地资源管理", "304"),
        ("物业服务与管理", "304"),
        ("医疗卫生", "284"),
        ("粉煤灰污染", "284"),
        ("占道", "284"),
        ("供热发展", "254"),
        ("农村土地规划管理", "254"),
        ("生活噪音", "253"),
        ("供热单位影响", "253"),
        ("城市供电", "223"),
        ("房屋质量与安全", "223"),
        ("大气污染", "223"),
        ("房屋安全", "223"),
        ("文化活动", "223"),
        ("拆迁管理", "223"),
        ("公共设施", "223"),
        ("供气质量", "223")]
    wordcloud = (
        WordCloud()
            .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud


@FACTORY.collect('timeline_bar')
def create_timeline_bar():
    family_types = [
        '一人户', '二人户', '三人户', '四人户', '五人户', '六人户', '七人户', '八人户', '九人户', '十人及其以上'
    ]
    data = [
        [1982, 7.7, 8.2, 12.2, 17.1, 18.4, 14.7, 10.1, 11.6, 0, 0],
        [1990, 5.8, 8.6, 16.8, 23.6, 21.4, 11.8, 5.9, 2.9, 1.4, 1.8],
        [2000, 9.1, 15.5, 25.4, 24.7, 15.8, 5.9, 2.2, 0.8, 0.3, 0.3],
        [2010, 12.1, 17.2, 24.3, 21.7, 13.7, 6.4, 2.6, 1.1, 0.5, 0.4],
        [2020, 27.3, 26.3, 19.4, 14.2, 6.9, 4, 1.1, 0.4, 0.2, 0.2]
    ]
    tl = Timeline()
    for item in data:
        year = item[0]
        bar = (
            Bar()
                .add_xaxis(family_types).add_yaxis('百分比(%)', item[1:])
                .set_global_opts(title_opts=opts.TitleOpts("福建省历年家庭户类型构成-{}年".format(year)))
        )
        tl.add(bar, "{}年".format(year))
    return tl


@FACTORY.collect('map_3d')
def create_map_3d():
    example_data = [
        [[119.107078, 36.70925, 1000], [116.587245, 35.415393, 1000]],
        [[117.000923, 36.675807], [120.355173, 36.082982]],
        [[118.047648, 36.814939], [118.66471, 37.434564]],
        [[121.391382, 37.539297], [119.107078, 36.70925]],
        [[116.587245, 35.415393], [122.116394, 37.509691]],
        [[119.461208, 35.428588], [118.326443, 35.065282]],
        [[116.307428, 37.453968], [115.469381, 35.246531]],
    ]
    c = (
        Map3D()
            .add_schema(
            maptype="山东",
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                is_main_shadow=False,
                main_alpha=55,
                main_beta=10,
                ambient_intensity=0.3,
            ),
            view_control_opts=opts.Map3DViewControlOpts(center=[-10, 0, 10]),
            post_effect_opts=opts.Map3DPostEffectOpts(is_enable=False),
        )
            .add(
            series_name="",
            data_pair=example_data,
            type_=ChartType.LINES3D,
            effect=opts.Lines3DEffectOpts(
                is_show=True,
                period=4,
                trail_width=3,
                trail_length=0.5,
                trail_color="#f00",
                trail_opacity=1,
            ),
            linestyle_opts=opts.LineStyleOpts(is_show=False, color="#fff", opacity=0),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-Lines3D")))
    return c
