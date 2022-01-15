# coding=utf8


from pyecharts import options as opts
from pyecharts.charts import Bar, Kline, Map, Pie, WordCloud


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


@FACTORY.collect('kline')
def create_simple_kline():
    data = [
        [2320.26, 2320.26, 2287.3, 2362.94],
        [2300, 2291.3, 2288.26, 2308.38],
        [2295.35, 2346.5, 2295.35, 2345.92],
        [2347.22, 2358.98, 2337.35, 2363.8],
        [2360.75, 2382.48, 2347.89, 2383.76],
        [2383.43, 2385.42, 2371.23, 2391.82],
        [2377.41, 2419.02, 2369.57, 2421.15],
        [2425.92, 2428.15, 2417.58, 2440.38],
        [2411, 2433.13, 2403.3, 2437.42],
        [2432.68, 2334.48, 2427.7, 2441.73],
        [2430.69, 2418.53, 2394.22, 2433.89],
        [2416.62, 2432.4, 2414.4, 2443.03],
        [2441.91, 2421.56, 2418.43, 2444.8],
        [2420.26, 2382.91, 2373.53, 2427.07],
        [2383.49, 2397.18, 2370.61, 2397.94],
        [2378.82, 2325.95, 2309.17, 2378.82],
        [2322.94, 2314.16, 2308.76, 2330.88],
        [2320.62, 2325.82, 2315.01, 2338.78],
        [2313.74, 2293.34, 2289.89, 2340.71],
        [2297.77, 2313.22, 2292.03, 2324.63],
        [2322.32, 2365.59, 2308.92, 2366.16],
        [2364.54, 2359.51, 2330.86, 2369.65],
        [2332.08, 2273.4, 2259.25, 2333.54],
        [2274.81, 2326.31, 2270.1, 2328.14],
        [2333.61, 2347.18, 2321.6, 2351.44],
        [2340.44, 2324.29, 2304.27, 2352.02],
        [2326.42, 2318.61, 2314.59, 2333.67],
        [2314.68, 2310.59, 2296.58, 2320.96],
        [2309.16, 2286.6, 2264.83, 2333.29],
        [2282.17, 2263.97, 2253.25, 2286.33],
        [2255.77, 2270.28, 2253.31, 2276.22],
    ]

    kline = (
        Kline()
            .add_xaxis(["2017/7/{}".format(i + 1) for i in range(31)])
            .add_yaxis("kline", data)
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_scale=True),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="Kline-基本示例"),
        )
    )
    return kline


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
