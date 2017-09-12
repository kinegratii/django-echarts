# 更新日志

## Dev

- js管理插件
    - 增加 `process_js_list` js合并函数
- js下载工具
    - 增加多文件下载支持
- 构建
    - 增加Django分类标记
    - 修正Django包依赖名称

## v0.1.1 (20170911)

- 新增 `SimpleEchartsView` 后端渲染视图类
- 新增 `echarts_container` ECharts容器模板标签
- 重写 `HostStore` 内部逻辑，支持自定义扩展host
- 下载命令支持js_host自定义参数
- `lib_js_host`和`map_js_host`支持 `local_host`变量引用
- 移除 `echarts_js` 模板标签
- 修正未设置 `settings.STATIC_URL`时host构建错误的bug

## v0.1.0 (20170906)

- 新增JS静态文件配置
- 新增远程JS文件下载命令
- 新增模板标签模块
- 新增API文档

## v0.0.1 (20170729)

- 发布试验版本