# 设计与实现

本文介绍了 django-echarts 的软件设计思想、体系和编程实现。

## 包体系设计

v0.5.1版本在保持整体公共访问接口不变的基础上，进一步重构底层实现逻辑。目前按照代码包可划分为以下模块：

| 代码包/模块                 | 描述                                     | 备注 |
| --------------------------- | ---------------------------------------- | ---- |
| **配置层**                  |                                          |      |
| django_echarts.core         | 依赖项、主题配置                         |      |
| django_echarts.conf         | 配置访问入口                             |      |
| **数据层**                  |                                          |      |
| django_echarts.entities     | 组件定义层                               |      |
| django_echarts.stores       | 组件全局存储入口                         |      |
| **模板层**                  |                                          |      |
| django_echarts.contrib      | 内置的主题APP                            |      |
| django_echarts.templates    | 模板文件                                 |      |
| **渲染层**                  |                                          |      |
| django_echarts.renders      | 组件、依赖项渲染逻辑                     |      |
| django_echarts.templatetags | 标签函数                                 |      |
| **视图业务层**              |                                          |      |
| django_echarts.starter      | 网站视图路由层                           |      |
| django_echarts.views        | 普通视图层                               |      |
| **功能扩展**                |                                          |      |
| django_echarts.ajax_echarts | ajax方式渲染echarts图表逻辑 <sup>1</sup> |      |
| django_echarts.management   | 命令行工具                               |      |
| django_echarts.geojson      | geojson工具层                            |      |

1. 截至v0.5.x，该功能暂未实现。



## 单元测试

django-echarts 坚持保证代码质量，包括 Typing Hints 、单元测试、代码覆盖率等工具和方法。

单元测试位于项目目录 `tests` （包含 `__init__.py` 文件，视为一个包）。
