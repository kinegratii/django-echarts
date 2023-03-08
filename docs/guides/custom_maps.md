# 自定义地图

> Add in 0.6.0
>
> Update in 0.6.0:  django_echarts.geojson 模块已标记为废弃。

## 概述

django-echarts 支持echarts的自定义地图（由 `registerMap` 注册的地图），具体包括 geojson 和 svg 两种。

| django-echarts | echarts版本           | 支持类型     | 支持模块                     |
| -------------- | --------------------- | ------------ | ---------------------------- |
| 0.5.x          | pyecharts1.9/echarts4 | geojson      | `django_echarts.geojson`     |
| 0.6.x          | pyecharts1.9/echarts4 | geojson      | `django_echarts.custom_maps` |
|                | pyecharts2.0/echarts5 | geojson、svg | `django_echarts.custom_maps` |

和 pyecharts 使用内嵌方式不同的是，django-echarts 全部采用外链方式，不支持内嵌方式，即 `Map.add_geo_json` 方法在 django-echarts 不可用。

## 函数 API

```python
django_echarts.custom_maps.use_custom_map(chart_obj, map_name:str, url:str)
```

该函数将替代 pyecharts 中的 `add_geo_json`。为某个图表对象添加自定义地图，一个地图对象只能添加一个。各参数意义如下：

| 参数      | 描述                                                  |
| --------- | ----------------------------------------------------- |
| chart_obj | pyecharts图表对象                                     |
| map_name  | 字符串。地图名称，`echarts.regiterMap` 的第一个参数。 |
| url       | 字符串。远程地址或本地地址                            |

需要注意的是：

第一，在 pyecharts1.9/echarts4时，不支持 svg格式。

第二，在使用时必须由使用者确定地图类型是 geojson 还是 svg。规则是 `name` 和 `url` 至少有一个以 `.geojson` 、`.json`、 `.svg` 结尾。

```python
use_custom_map(chart_obj, '福建省地图', 'https://geo.datav.aliyun.com/areas_v3/bound/350000_full.json')
use_custom_map(chart_obj, '福建市县地图', '/geojson/fujian.geojson')
use_custom_map(chart_obj, 'flight_seats', '/svg/flight_seats.svg')

use_custom_map(chart_obj, 'flight_seats', '/svg/flight_seats') # 错误的使用
```

不符合以上两个条件时将抛出 `ValueError` 异常。

## 远程地图引用

远程地图使用比较简单，参数 url 直接使用即可

## 本地地图引用

配置

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
]

DJANGO_ECHARTS = {
    'repos':{'local':f'{STATIC_URL}assets/'}
}
```

