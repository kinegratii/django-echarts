# 依赖项和静态文件

## 概述

v0.5.x重新实现了这一模块。主要特点：

- 完全兼容 pyecharts 静态文件逻辑，不再区分 lib/map 类型。

## 在线引用

django-echarts默认使用 pyecharts 作为默认源。

## 本地化资源



下载依赖

```
python manage.py dms --action=show echarts fujian
python manage.py dms --action=download echarts fujian
```

