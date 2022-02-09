# 开发协作

## Q&A

**1 django-echarts支持pycharts哪些图表类型？**

目前 django-echarts不支持以下图表类型

- 表格 `pyecharts.components.Table`
- 选项页 `pyecharts.charts.Tab`
- 百度地图 `pyecharts.charts.BMap`



## 问题反馈

请使用Github Issues 描述你的问题。

## 参与开发

在参与开发之前，您必须确保：

- 掌握 Python Typing Hints 相关内容
- 熟悉Django框架的有关内容，包括但不限于路由、模板系统、CBV等
- 熟悉pyecharts库的功能，以及核心实现逻辑

## 开发方向

- 【图表类型】支持更多的图表类型，如组合图表、时序图表等。
- 【模板引擎】目前仅使用DTE渲染HTML页面，希望兼容jinja2模板引擎，这样完全可以利用pyecharts的相关逻辑。
- 【数据处理】基于 Django Model的数据预处理。
- 【UI框架扩展标准】通过进一步抽象UI框架渲染逻辑，使得能够更好地支持现有的其他主流UI框架。
- 【版本特性兼容】关注Django和pyecharts的重大版本更新，能够兼容更多的版本组合。



