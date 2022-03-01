# 依赖项和静态文件

## 概述

django-echarts 本身不携带任何静态文件，默认引用在线资源，可以通过提供的命令下载到本地。

这些资源包括：

- echarts库文件
- echarts地图文件
- echarts主题文件
- UI主题文件

django-echarts的依赖项模块对 pyecharts 作了进一步扩展：

- 完全兼容 pyecharts 仓库引用逻辑。
- 支持自定义单项引用
- 提供下载命令以支持本地化。

django-echarts 和 pyecharts 共用底层静态文件存储字典 ，具体可参见 `pyecharts.datasets` 包。

## 仓库源

> DJEOpts.dms_repo:str = 'pyecharts'

django-echarts默认使用 pyecharts-asserts 作为默认源。

```python
DJANGO_ECHARTS = DJEOpts(
    echarts_version='4.8.0',
    dms_repo='pyecharts',
)
```

django-echarts 内置下列仓库源。

| 引用标识  | 仓库URL                              | 备注                                                       |
| --------- | ------------------------------------ | ---------------------------------------------------------- |
| pyecharts | https://assets.pyecharts.org/assets/ | 在线引用                                                   |
| local     | /static/assets/                      | 使用django静态文件托管，需要通过下载器先下载到项目目录之下 |

可以将 dms_repo 参数设置为你的远程仓库url，关于如何组织仓库内部目录结构，请参考 pyecharts 相关文档。

## 自定义依赖项

> DJEOption:dep2url = {}

django-echarts 支持对单个依赖进行单独引用，dep2url 的配置优先于上述的 dms_repo 配置。

```python
DJANGO_ECHARTS = {
    'dep2url':{
        'echarts': 'https://cdnjs.cloudflare.com/ajax/libs/echarts/4.8.0/echarts.min.js',
        'echarts-gl': 'https://assets.pyecharts.org/assets/echarts-gl.min.js'
    }
}
```

对于一些常用的依赖项（主要指的是 echarts 和jquery），可以使用 `#CDN` 方式引用。

```python
DJANGO_ECHARTS = {
    'dep2url':{
        'echarts': '#cdnjs',
        'echarts-gl': '#pyecharts'
    }
}
```

## 本地化资源

django-echarts提供了一个下载器（命令行工具），支持本地化。

### 查看依赖项信息

查看某个依赖项的具体信息

```text
E:\projects\zinc>python manage.py info -d echarts
[File #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
```

三行信息分别是：

- 远程url，下载远程。
- Django项目，本地引用url。
- 最后一行是本地实际文件路径，文字颜色表示是否存在该文件。

查看多个依赖项的信息。

```text
E:\projects\zinc>python manage.py info -d echarts 福建
[File #01] echarts; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/echarts.min.js
        Static Url: /static/echarts.min.js
        Local Path: E:\projects\zinc\static\echarts.min.js
[File #02] 福建; Catalog: Dependency
        Remote Url: https://assets.pyecharts.org/assets/maps/fujian.js
        Static Url: /static/maps/fujian.js
        Local Path: E:\projects\zinc\static\maps\fujian.js
```



### 下载依赖项文件

下载一个或多个依赖项

```text
python manage.py download -d echarts fujian
```



