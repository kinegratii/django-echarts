# UI框架和主题

界面主题包括UI框架和调色主题。

## 内置UI框架

django-echarts内置以下主题：

| 标识符              | 文件                                   | 备注    |
| ------------------- | -------------------------------------- | ------- |
| bootstrap3          | /static/css/bootstrap3.min.js          | v0.5.0+ |
| bootstrap3.cerulean | /static/css/bootstrap3.cerulean.min.js | v0.5.0+ |
| material            | /static/css/materal.min.js             | v0.5.0+ |

css文件由 [Bootswitch](https://bootswatch.com/3/) 构建。 



## 自定义调色主题

django-echarts还支持自定义UI框架的调色主题。

以 bootstrap3为例，首先需要从 https://bootswatch.com/3/ 下载对应调色的css文件修改文件名称，放在static目录下，并将palette_css指向这个css文件。

```python
DJE_SITE = {
    'theme': {
        'bootstrap3':{
            'palette_css': '/static/bootstrap3/bootstrap3.flatly.min.css'
        }
    }
}
```

## 自定义UI框架

（此功能暂未实现.）



## 注册视图

当需要在某个页面实现自己的逻辑时，可以继承相应的实现视图类，重写相关属性和方法，然后调用对应的方法注册到 site_obj 对象之中。

```python
DJESite.register_home_view(view_class: Type[DJESiteHomeView])
DJESite.register_list_view(view_class: Type[DJESiteListView])
DJESite.register_detail_view(view_class: Type[DJESiteDetailView])
DJESite.register_about_view(view_class: Type[DJESiteAboutView])
```

一般来说，诸如Home/List/About等仅显示静态数据的页面，`DJESite` 提供了更为简洁的方式实现，而不必显式调用这些注册函数。比如 `DJESite.paginate_by` 属性等。

## 自定义模板文件

所有的视图类均继承 `django.views.generic.base.TemplateView` ，因此可以通过重写 `template_name` 重新指定相应的模板文件。

另外，一些视图（如DJESiteListView和DJESiteDetailView）会使用到不同的模板文件，这些变量名称通常以 `*_template_name` 的方式存在。

```python
class MyChartDetailView(DJESiteDetailView):
    template_name = 'my_detail.html'
    empty_template_name = 'my_empty.html'
```

指定的模板文件名称可以是具体字符串，也可以是待赋值的字符串，比如 `'{theme}/home.html'`。Site将传入下列变量：

- theme: 主题名称