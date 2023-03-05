# 依赖项(一)：基本配置

django-echarts的依赖项模块对 pyecharts 作了进一步扩展：

- 完全兼容 pyecharts 仓库引用逻辑。
- 支持混合仓库源，可对单个依赖项单独引用。
- 提供一系列生产力命令和界面支持仓库源切换和依赖项检测。

## 基本概念

### 依赖项

依赖项，渲染html图表所需要的javascript库文件和数据文件，具体来说：

| 类别                      | 文件格式              | 支持版本设置 | 默认仓库源 | 描述                      |
| ------------------------- | --------------------- | ------------ | ---------- | ------------------------- |
| echarts及其扩展           | js                    | 是           | pyecharts  | echarts核心及其扩展库     |
| echarts主题文件           | js                    | 否           | pyecharts  | echarts主题文件           |
| pyecharts地图<sup>1</sup> | js                    | 否           | pyecharts  | 由pyecharts托管的数据文件 |
| 自定义地图<sup>2</sup>    | json、svg<sup>3</sup> | 否           | 需自行指定 | geojson/svg底图           |

注：

1. 原为echarts内置地图，echarts5.x不再内置。
2. 相关接口由 django-echarts封装。
2. svg格式仅pyecharts2.0/echarts5.4以上支持

每个依赖项(参见`django_echarts.core.localfiles.DownloaderResource`)拥有的属性如下：。

| 属性       | 类型 | 描述         |
| ---------- | ---- | ------------ |
| dep_name   | str  | 依赖项名称   |
| remote_url | str  | 远程地址     |
| ref_url    | str  | 引用路径     |
| local_path | str  | 本地文件路径 |

django-echarts 和 pyecharts 共用底层静态文件存储字典 ，具体可参见 `pyecharts.datasets` 包。

### 仓库源

> DJEOpts.dms_repo:str = 'pyecharts'
>
> DJEOpts.echarts_version = '4.8.0'

仓库源，存储依赖项实际的网络或本地目录，可通过url访问，其中本地目录由django staticfile或其他apache等服务器托管。仓库源使用 `#repo` 形式标识。

一个完整的仓库目录如下，参见 pyecharts-asserts：

```
assets/
  |- maps/
    |- china.js
  |- themes/
    |- white.js
  echarts.min.js
  echarts-wordcloud.min.js
  jquery.min.js
```

django-echarts默认使用网络仓库源。

```python
DJANGO_ECHARTS = DJEOpts(
    echarts_version='4.8.0',
    dms_repo='pyecharts',
)
```

### 内置仓库

django-echarts 内置下列仓库源。

| 引用标识     | 仓库URL                                 | 备注                                                         |
| ------------ | --------------------------------------- | ------------------------------------------------------------ |
| pyecharts    | https://assets.pyecharts.org/assets/    | 基于echarts4.8的仓库                                         |
| pyecharts-v5 | https://assets.pyecharts.org/assets/v5/ | 基于echarts5.4的仓库                                         |
| local        | `{STATIC_URL}assets/`                   | 使用django静态文件托管，路径前缀由 `settings.STATIC_URL` 确定 |

各个仓库所包含的文件如下：



| 类别            | pyecharts | pyecharts-v5 | unpkg | local    |
| --------------- | --------- | ------------ | ----- | -------- |
| echarts及其扩展 | √         | √            | √     | 用户指定 |
| echarts主题文件 | √         | √            |       | 用户指定 |
| pyecharts地图   | √         | √            |       | 用户指定 |
| 自定义地图      |           |              |       | 用户指定 |

注：

## 自定义依赖项

> DJEOption.dep2url = {}

### 基本设置

django-echarts 支持对单个依赖进行单独引用，dep2url 的配置优先于上述的 dms_repo 配置。

`dep2url`为字典形式，其中 key 为依赖项名称，value 为对应文件引用的 url 或仓库标签。

在一些情况，对于某些文件可以改用其他仓库源。比如，在下面例子下除了 `dep2url` 之外其他依赖项均引用 pyecharts 的资源。

```python
DJANGO_ECHARTS = {
    'dms_repo':'pyecharts',
    'dep2url':{
        'echarts-wordcloud': 'https://unpkg.com/echarts-wordcloud@1.1.4/dist/echarts-wordcloud.min.js',
        'china':'#local',
        'fujian_cities_map':'/static/assets/maps/fujian_cities_map.js'
    }
}
```

说明：

- pyecharts上的 echarts-wordcloud版本为1.1.3，如果后续发布的1.1.4版本解决了1.1.3的一些影响使用的bug，可以通过上述方法改用1.1.4版本。
- 如果中国地图文件 *china.js* 是经常使用的，可以先下载到本地，再使用 `#local` 改用本地的文件。

### 批量设置

> Add in 0.6.0

`dep2url` 支持批量设置

```python
DJANGO_ECHARTS = {
    'dep2url':{
        '#local': ['echarts', 'china']
    }
}
# 等效于

DJANGO_ECHARTS = {
    'dep2url':{
        'echarts': '#local',
        'china': '#local'
    }
}
```



## 默认值

django-echarts 0.6.x + pyecharts2.0默认配置如下：

```python
{
    'echarts_version': '5.4.1',
    'dms_repo': 'pyecharts-v5',
    'dep2url':{}
}
```

django-echarts 0.6.x + pyecharts1.9默认配置如下：

```python
{
    'echarts_version': '4.8.0',
    'dms_repo': 'pyecharts',
    'dep2url':{}
}
```

django-echarts 0.5.x + pyecharts1.9默认配置如下：

```python
{
    'echarts_version': '4.8.0',
    'dms_repo': 'pyecharts',
    'dep2url':{}
}
```

