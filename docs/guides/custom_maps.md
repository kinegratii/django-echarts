# 自定义地图

> Add in 0.6.0
>

## 概述

### 功能支持

django-echarts 支持echarts的自定义地图（由 `registerMap` 注册的地图），包括 geojson 和 svg 两种类型。

| django-echarts | echarts版本           | 支持类型     | 支持模块                     |
| -------------- | --------------------- | ------------ | ---------------------------- |
| 0.5.x          | pyecharts1.9/echarts4 | geojson      | `django_echarts.geojson`     |
| 0.6.x          | pyecharts1.9/echarts4 | geojson      | `django_echarts.custom_maps` |
|                | pyecharts2.0/echarts5 | geojson、svg | `django_echarts.custom_maps` |

### 模板渲染：内嵌VS外链

**pyecharts**: pyecharts  使用内嵌方式，函数 `Map.add_geo_json(geo_json:dict)` 传入的是 geojson数据本身。geojson内容读取在python端实现。

```python
geo_json = {<geojson_data>}

(
    Map()
    .add(
        series_name="商家A",
        data_pair=[list(z) for z in zip(Faker.provinces, Faker.values())],
        maptype="custom_geo_json",
    )
    .add_geo_json(geo_json=geo_json)
    .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .render()
)
```

**django-echarts** : django-echarts 全部采用外链方式，不支持内嵌方式。`use_costom_map` 第三个参数传入的是geojson文件的DataURL或与DataURL关联的文件名称。geojson内容读取在javascript通过ajax读取。

```python
chart_obj = (
    Map()
    .add(
        series_name="商家A",
        data_pair=[list(z) for z in zip(Faker.provinces, Faker.values())],
        maptype="福建省地图",
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
use_custom_map(chart_obj, '福建省地图', 'https://geo.datav.aliyun.com/areas_v3/bound/350000_full.json')
```

### 文件路由：DataURL VS FileURL

对于一个geojson或svg文件，有DataURL 和 FileURL 之分。

| 区分                  | FileURL                    | DataURL                                                    |
| --------------------- | -------------------------- | ---------------------------------------------------------- |
| Rsponse内容           | 二进制文件                 | 文件内容，字符串或json格式                                 |
| Response Content Type | `application/octet-stream` | `application/json` (适用geojson) 或 `text/plain` (适用svg) |
| 视图处理模块          | `django.staticfiles`       | `django_echarts.custom_maps`                               |

## 函数use_custom_map

### 使用方法

```python
django_echarts.custom_maps.use_custom_map(chart_obj, map_name:str, url_or_filename:str='')
```

该函数作用类似于 pyecharts 中的 `add_geo_json`，为某个图表对象添加自定义地图，一个地图对象只能添加一个。各参数意义如下：

| 参数            | 描述                                                  |
| --------------- | ----------------------------------------------------- |
| chart_obj       | pyecharts图表对象                                     |
| map_name        | 字符串。地图名称，`echarts.regiterMap` 的第一个参数。 |
| url_or_filename | 字符串。远程地址或本地地图文件名                      |

需要注意的是：

第一，参数 `map_name` 必须和 关联图表的` maptype` 配置保持一致，否则无法正确加载底图。

第二，在 pyecharts1.9/echarts4时，不支持 svg格式。

第三，在使用时必须由使用者确定地图类型是 geojson 还是 svg。规则是 `name` 和 `url` 至少有一个以 `.geojson` 、`.json`、 `.svg` 结尾。

```python
use_custom_map(chart_obj, '福建省地图', 'https://geo.datav.aliyun.com/areas_v3/bound/350000_full.json')
use_custom_map(chart_obj, '福建市县地图', 'fujian.geojson')
use_custom_map(chart_obj, 'flight_seats', '/custom_maps/flight_seats.svg')

use_custom_map(chart_obj, 'flight_seats', 'flight_seats') # 错误的使用
```

不符合以上两个条件时该函数将抛出 `ValueError` 异常。

### 参数url_or_filename

参数 `url_or_filename` 支持以下方式的字符串：

| 地图引用方式   | 赋值要求                                        | 描述                     |
| -------------- | ----------------------------------------------- | ------------------------ |
| 按URL引用      | url 以 `https://` 或 `http://` 开头             | 引用远程地图<sup>1</sup> |
| 按filename引用 | 文件名，不以`/` 开头，以`.geojson` 或`.svg`结尾 |                          |
|                | 空值                                            | 默认同 `map_name`        |

备注：

1. 该 url 必须是 DataURL。即浏览器打开该url时可以查看其文件内容，而不是执行下载该文件。



## 文件名引用

```
filename ---(django_echarts.custom_maps)--> DataURL ----> FileURL --(django.staticfiles)--> file path
```



文件名引用方式依赖于 `django.staticfiles`。对于每一个地图文件，FileURL 和 DataURL 对应关系如下：

| URL类型 | 链接格式                                    | 说明                                                         |
| ------- | ------------------------------------------- | ------------------------------------------------------------ |
| FileURL | `{STATIC_URL}assets/custom_maps/{filename}` | 由 `django.staticfiles` 处理，返回 `HttpFileResponse`        |
|         | `{STATIC_URL}/geojson/{filename}`           | 仅兼容0.5.0，不再推荐适用                                    |
| DataURL | `/map_data/{filename}`                      | 由 `django_echarts.custom_maps` 处理，返回 `JSONResponse` 或 `HttpResponse` |

## 完整示例

第一步，准备地图数据文件 *china_cities.geojson*。

第二步，在图表中添加地图配置。下面两种写法基本是等效的，区别在于 `echarts.registrMap` 第一个参数值，不过这不影响开发和运行。

```python
use_custom_map(map_name='中国省市地图', url_or_filename='china_cities.geojson')
use_custom_map(map_name='china_cities.geojson')
```

第三步，确定  *china_cities.geojson* 放置的路径。

假定项目的 *settings.py* 配置如下：

```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)
```

则项目目录结构及geojson文件路径如下：

```text
- zinc/
  |- zinc/
    |- settings.py
    |- urls.py
  |- static/
    |- assets/
      |- maps/
        |- china.js
      |- custom_maps/
        |- china_cities.geojson # <--- 文件路径
```

