# 配置

## 定义

django-echarts 遵循统一配置的原则，所有的配置均定义在项目配置模块一个名为 `settings.DJANGO_ECHARTS` 变量中，该变量可以指向

- 一个`dict`对象
- `django_echarts.dms.core.DJEOpts` 对象

例子( *settings.py*)

```python
DJANGO_ECHARTS = {
    'echarts_version': '4.8.0',
    'lib_repo': 'bootcdn',
    'map_repo': 'pyecharts'
}

# 或者

from django_echarts.core.dms import DJEOpts

DJANGO_ECHARTS = DJEOpts(
    echarts_version='4.8.0',
    lib_repo='cdnjs',
    map_repo='pyecharts',
)
```

## DJEOpts类

### echarts_version

```python
DJEOpts.echarts_version: str = '4.8.0'
```

echarts的版本，需根据 pyecharts 项目确定。

### lib_repo

```python
DJEOpts.lib_repo: str = 'cdnjs'
```

echarts库文件的远程CDN仓库。默认情况下，下列文件属于库文件，否则属于地图库文件。

```
[
    'echarts.common', 'echarts.common.min',
    'echarts', 'echarts.min',
    'echarts.simple', 'echarts.simple.min',
    'extension/bmap', 'extension/bmap.min',
    'extension/dataTool', 'extension/dataTool.min'
]
```

可选值如下：

| repo_name | repo_url |
| ---- | ---- |
| pyecharts | https://assets.pyecharts.org/assets/ |
| cdnjs | https://cdnjs.cloudflare.com/ajax/libs/echarts/{echarts_version} |
| npmcdn | https://unpkg.com/echarts@{echarts_version}/dist |
| local | 使用django静态文件托管 |

repo_url中echarts_version变量的值由 `DJEOpts.echarts_version` 确定。

### map_repo

```python
DJEOpts.map_repo: str = 'pyecharts'
```

地图库文件的远程CDN仓库。

可选值如下：

| repo_name | repo_url |
| ---- | ---- |
| pycharts | https://assets.pyecharts.org/assets/maps/ |
| china-provinces | https://echarts-maps.github.io/echarts-china-provinces-js/ |
| china-cities | https://echarts-maps.github.io/echarts-china-cities-js/ |
| united-kindom | https://echarts-maps.github.io/echarts-united-kingdom-js |
| local | 使用django静态文件托管 |

### local_dir

略

### lib_local_dir

略

### map_local_dir

略

### file2map

```python
DJEOpts.file2map: Dict[str, Union[dict, str]]
```

自定义 dependency 的映射规则。具体参见下文的 *自定义映射规则* 部分。


## 静态文件映射

### 基本规则

django-echarts 单独实现了自己的静态文件映射模块。对于每一个pycharts图表，根据lib_repo/map_repo 的设置，引用相应的javascript文件。

默认规则如下：

```python
def resolve_url(repo_url, dep_name):
    return repo_url.format(echarts_version=opts.echarts_version) + dep_name + '.js'
```

例子：当lib_repo=“npmcdn” 时，名称为 echarts 的js_dependency 对应的文件url是  https://unpkg.com/echarts@4.8.0/dist/echarts.min.js。

### 自定义映射规则

可以通过 `DJEOpts.file2map` 编写自定义映射规则。

```
file2map = {
    'dep_name1': 'url',
    'dep_name2': '@dep_name3',
    '#repo_name1': 'url',
    '#repo_name2': {
        'dep_name5': '@dep_name6',
        'dep_name6': 'url'
    }
}
```

- 例子一，新增CDN仓库。字典key的仓库名称前面需要添加`#`以表明这是一个仓库。

```python
file2map = {
    '#mycdn': 'https://staticfiles.mycdn.com/dist/'
}
```

- 例子二，新增的CDN中lib和map分属不同的url，可以在仓库名称之后加上 .lib/.map 以示区别。

```python
file2map = {
    '#mycdn.lib': 'https://staticfiles.mycdn.com/dist/lib/',
    '#mycdn.map': 'https://staticfiles.mycdn.com/dist/map/',
}
```

- 例子三：对已有仓库进行patch操作，用于仓库缺失某些文件的情况，引用其他dependency。如，pycharts仓库有 echarts.js 文件，但是没有对应的echarts.min.js 文件。

```python
file2map = {
    '#pyecharts': {'echarts': '@echarts.min'}
} 
```

说明： `#pycharts` 标识是名为 pyecharts 的仓库，`@echarts.min` 表示 echarts 引用同仓库内echarts.min对应的文件。

- 例子四：仓库缺失某些文件，自定义url。

```python
file2map = {
    '#pyecharts': {'echarts': '{url}dev/echarts.min.js'}
} 
```

### 本地映射

略

### 映射顺序

按照下列算法决定远程 url。 **对于远程url，映射模块不检查该url是否可访问，只要匹配到即返回。**

```text
输入: 
  repo_name 仓库名称
  dep_name 依赖项名称

过程:
  dep_name:url
  dep_name:@dep_name2
  #repo_name: {dep_name:url}
  #repo_name: {dep_name:@dep_name3}
```