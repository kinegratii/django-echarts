# coding=utf8

import json

from pyecharts import Bar, Kline, Map, Pie, WordCloud


def create_simple_bar():
    bar = Bar("我的第一个图表", "这里是副标题")
    bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
    bar.renderer = 'svg'
    return bar


def create_simple_kline():
    v1 = [[2320.26, 2320.26, 2287.3, 2362.94],
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
          [2255.77, 2270.28, 2253.31, 2276.22]]

    kline = Kline("K 线图示例")
    kline.add("日K", ["2017/7/{}".format(i + 1) for i in range(31)], v1)
    kline.renderer = 'svg'
    return kline


def create_simple_map():
    value = [155, 10, 66, 78]
    attr = ["福建", "山东", "北京", "上海"]
    map1 = Map("全国地图示例", width=1200, height=600)
    map1.add("", attr, value, maptype='china')
    map1.renderer = 'svg'
    return map1


def create_simple_pie():
    pie = Pie('各类电影中"好片"所占的比例', "数据来着豆瓣", title_pos='center')
    pie.add("", ["剧情", ""], [25, 75], center=[10, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, )
    pie.add("", ["奇幻", ""], [24, 76], center=[30, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, legend_pos='left')
    pie.add("", ["爱情", ""], [14, 86], center=[50, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["惊悚", ""], [11, 89], center=[70, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["冒险", ""], [27, 73], center=[90, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["动作", ""], [15, 85], center=[10, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["喜剧", ""], [54, 46], center=[30, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["科幻", ""], [26, 74], center=[50, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["悬疑", ""], [25, 75], center=[70, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["犯罪", ""], [28, 72], center=[90, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, is_legend_show=True, legend_top="center")
    pie.renderer = 'svg'
    return pie


def create_word_cloud():
    name = [
        'Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
        'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
        'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
        'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
    value = [
        10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
        965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", name, value, word_size_range=[20, 100])
    print(json.dumps(wordcloud.options, indent=4))
    return wordcloud
