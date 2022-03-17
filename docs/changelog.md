# 更新日志

## v0.5.0 - (20220320)

- 使用主题独立APP架构，修改主题设置方式
- 新增直接支持 `prettytable.PrettyTable` 表格类型
- 新增支持自定义geojson地图
- 命令 info / download / starttpl 可忽略 `--theme` 参数，默认为 `INSTALLED_APPS` 配置的主题。
- 新增 *blank.html* 空白模板文件。
- Nav组件新增底部链接列表。
- 新增设置(settings)页面。
- 支持以表单方式更换调色主题。
- 导航栏文字支持模板字符串 `DwString`
- 导航栏支持是否固定设置
- Borax更新至v3.5.3

## v0.5.0b2 - (20220306)

- 列表页面支持关键字搜索
- 优化列表页分页组件
- 首页jumbotron组件支持使用图表显示
- 新增支持Bootstrap5框架，默认采用Bootstrap5框架
- 新增内置支持 Bootstrap框架的16个调色主题
- 新增查看echarts图表options功能
- 新增支持pyecharts在线地图
- 新增支持3D图表
- 新增支持 pyecharts Table 表
- 新增 WidgetCollection图文合辑页面渲染
- 新增支持echarts主题
- 新增 info/download 命令行工具
- 新增 starttpl 命令工具
- 图表支持自动调整大小功能
- 移除 `listdep` 命令

## v0.5.0b1 - (20220212)

- 新增starter可视化网站生成器
- 首页新增热门推荐模块
- 列表页面支持grid布局
- 支持bootstrap3调色主题切换
- 新增支持Materialcss框架

## v0.5.0a1 - (20220110)

- 迁移支持 Python3.7+ / Django3.0+ / pyecharts1.9+