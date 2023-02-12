# 参数化图表

> Add in 0.6.0

从0.6.0开始，django-echarts 支持参数化图表，对于同一个图表，可以根据传入的数据参数，构建不同的图表，这些图表的配置是相同的，只是数据有所不同。

## 基础例子

实现一个参数化图表很简单，只需在图表注册函数添加参数即可。

```python
from django_echarts.entity.uri import ParamsConfig
from django_echarts.starter.sites import DJESite
from pyecharts import options as opts
from pyecharts.charts import Bar

site_obj = DJESite(site_title='福建统计')

@site_obj.register_chart(title='{year}年福建省家庭户类型组成', 
                        params_config=ParamsConfig({'year': [1982, 1990, 2000, 2010, 2020]}))
def yearly_family_types(year: int):
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
    yearly_data = {item[0]: item[1:] for item in data}
    if year not in yearly_data:
        raise ChartDoesNotExist(f'暂无{year}年数据')
    year_data = yearly_data[year]
    bar = (
        Bar()
            .add_xaxis(family_types).add_yaxis('百分比(%)', year_data)
            .set_global_opts(title_opts=opts.TitleOpts("福建省家庭户类型构成-{}年".format(year)))
    )
    return bar
```

### 定义图表参数

图表参数位于图表注册函数（为 `DJESite.register` 或 `EntityFactory.register` 所修饰的函数）的参数列表，你可以和正常函数一样定义任何参数。

django-echarts 推荐尽可能遵循下列明确性的规则：

- 为每个参数声明数据类型，在URL方式调用下能够将其转化为对应的数据类型值，目前仅支持 `int / float / str / UUID` 等构造函数为`type(s)`的数据类型。
- 不推荐使用 `*args` ，使用 `**kwags`。

### 定义关联ChartInfo

`DJESite.register` 或 `EntityFactory.register` 装饰器的三个参数 title，description，body支持模板字符串，如上述例子中的 `{year}年福建省家庭户类型组成`。

**注意：此处使用str.format的单括号形式，而不是Django模板的双括号形式。**

### 返回图表

如果用户输入的参数没有对应的图表，可以抛出 `ChartDoesNotExist` 异常。

### 参数配置ParamsConfig

`params_config` 用于定义可选参数项，仅用于无参数时的图表页面显示。

在构建图表对象时不会检查参数是否符合在此配置之中，因此在图表构建函数中仍需检查相应的参数，对不符合的情况抛出 `ChartDoesNotExist 异常`。

`params_config` 必须是支持下列接口的对象。

```python
class ParamsConfigMixin:
    def __iter__(self) -> Generator[dict, Any, None]:
        pass
```

如下列两种方式定义是等效的。

```python
pc1 = ParamsConfig([
    {'year':2021, 'month':1}, {'year':2021, 'month':2},
    {'year':2021, 'month':3}, {'year':2021, 'month':4}
])

pc2 = ParamsConfig({
    'year':[2021],
    'month':[1, 2, 3, 4]
})
```



## EntityURI

为统一标识django-echarts的实体（图表、组件）引入`ENtityURI` 类，该类的一个对象由类别(catalog)、名称(name)、参数(params)三部分组成。例如上述例子中2020年的资源标识可表示为：

```python
family_types_2020_uri = EntityURI(catalog='chart', name='yearly_family_types', params={'year':2020})
```

`EntityURI` 还有字符串形式，其格式如下:

```
<资源类别>:<资源名称>/<参数名称1>/<参数值1>/<参数名称2>/<参数值2>/<参数名称3>/<参数值3>/
```

在多个参数情况下，其参数顺序不受影响，因此一个图表可能有多个字符串标识。

例如：上述例子可表示为

```
chart:yearly_family_types/year/2020
```

关联的`ChartInfo`表示为

```
info:yearly_family_types/year/2020
```

字符串形式通常用于URL、合辑、页面组件构建。

```python
site_obj.add_widgets(jumbotron_chart='chart:yearly_family_types/year/2020') # 首页jumbotron位置显示2020年的数据




rc = RowContainer()
rc.add_widget('chart:yearly_family_types/year/2020')
rc.add_widget(EntityURI(catalog='chart', name='yearly_family_types', params={'year':2020}))
```

今年的数据总是

## 使用图表

### 从EntityFactory引用

所有的图表和HTML组件均存储在全局变量 `django_echarts.stores.entity_factory.factory` 中。`EntityFactory` 提供两种方式引用

```python
from django_echarts.stores.entity_factory import factory

family_types_chart_2020 = factory.get_chart_widget('yearly_family_types', params={'year':2020}) # 使用参数字典

family_types_chart_2020 = factory.get_widget_by_uri(family_types_2020_uri) # 使用uri方式
```

### 从ChartInfo引用

使用 `ChartInfo.uri` 属性。

