# 体系设计

本文介绍了 django-echarts 的软件设计思想、体系和编程实现。

## 包体系设计

v0.5.1版本在保持整体公共访问接口不变的基础上，进一步重构底层实现逻辑。目前按照代码包可划分为以下模块：

| 代码包/模块                  | 描述                        | 定位       |
| ---------------------------- | --------------------------- | ---------- |
| django_echarts.ajax_echarts0 | ajax方式渲染echarts图表逻辑 | 扩展层     |
| django_echarts.contrib       | 内置的主题APP               | 主题模板层 |
| django_echarts.core          | 依赖项、主题配置            | 配置定义层 |
| django_echarts.entities      | 组件定义层                  | 实体定义层 |
| django_echarts.management    | 命令行工具                  |            |
| django_echarts.renders       | 组件、依赖项渲染层          | 渲染层     |
| django_echarts.starter       | 网站视图路由层              | 视图层     |
| django_echarts.stores        | 组件存储层                  | 数据存储层 |
| django_echarts.templates     | 模板文件                    | 公用模板层 |
| django_echarts.templatetags  | 标签函数                    | 标签函数   |
| django_echarts.conf          | 配置访问层                  | 配置访问层 |
| django_echarts.geojson       | geojson工具层               | 扩展层     |
| django_echarts.views         | 普通视图层                  | 视图层     |

