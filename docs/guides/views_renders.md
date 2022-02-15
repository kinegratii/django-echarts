# 视图渲染

django_echarts 提供两种方式的渲染视图，即：

- 后端：通过模板标签/标签渲染页面
- 前端(前后端分离)：先渲染页面，数据通过 Ajax 异步请求返回

两者渲染方式具有共同的接口，均继承自 `django_echarts.views.base.EChartsMixin` 。

## 前端渲染


渲染需要继承 `EChartsFrontendView` 类，和后端渲染方式不同的是，该视图类返回是 `chart.options` 的 json 字符串，而前端需要使用 ajax 等方式接收数据，并且需要使用 setOption 函数设置信息。

```html
<script src="httpss://cdn.bootcss.com/echarts/3.6.2/echarts.min.js"></script>
<script src="https://echarts.baidu.com/asset/map/js/china.js"></script>
<script type="text/javascript">
    var mChart;
    function loadEcharts() {
        var url = '/options/simpleBar/';
        if (mChart != null) {
            mChart.clear();
        }
        mChart = echarts.init(document.getElementById('id_echarts_container'));
        mChart.showLoading();
        $.ajax({
            url: url,
            type: "GET",
            data: null,
            dataType: "json"
        }).done(function (data) {
            mChart.hideLoading();
            mChart.setOption(data);
        });
    }
    $(document).ready(function () {
        loadEcharts('simpleBar');
    });
</script>
```
## 后端渲染

略