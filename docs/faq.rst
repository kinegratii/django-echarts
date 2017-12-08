FAQ
=====

Q: django_echarts 对于 pyecharts 有什么改造？

A：首先需要明确的一点的是： django_echarts 仅使用了 pyecharts 当中的图表构建模块。基于此和 Django 开发最佳实践，对 pyecharts 的特性作了一定的调整，包括：

- jshost 不支持对象级别设置
- javascript 链接不支持内部嵌入方式引用



Q: 本地部署无法引用 echarts.js 文件 ？

A: 为了节省资源和提高加载效率，在 pyecharts 中 依赖文件 echarts 实际引用的是 echarts.min.js ，因此可以使用其压缩版本文件 echarts.min.js 代替， 请确保文件名是 echarts.min.js 。