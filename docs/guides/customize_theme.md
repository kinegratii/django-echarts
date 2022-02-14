# UI框架和主题

界面主题包括UI框架和调色主题。

## 内置UI框架

django-echarts内置以下主题：

| 标识符              | 文件                                          | 备注    |
| ------------------- | --------------------------------------------- | ------- |
| bootstrap3          | 在线引用                                      | v0.5.0+ |
| bootstrap3.cerulean | /static/bootstrap3/bootstrap3.cerulean.min.js | v0.5.0+ |
| bootstrap5          | 在线引用                                      | v0.5.0+ |
| material            | 在线引用                                      | v0.5.0+ |

## 自定义调色主题

django-echarts还支持自定义UI框架的调色主题。

以 bootstrap3为例，首先需要从 https://bootswatch.com/3/ 下载darkly对应调色的css文件，修改文件名称，放在static目录下。

```text
|-- static
    |-- bootstrap3.darkly.min.css
```



第二步，调用 `install_themes` 函数，字典键表示主题标识符，必须符合`<UI框架>` 或者 `<UI框架>.<调色>`的格式。

```python
from django_echarts.core.themes import install_themes

install_themes({
    'bootstrap3.darkly': {
        'palette_css': '/static/bootstrap3.darkly.min.css'
    }
})

site_obj = DJESite(
    site_title='图表可视化',
    theme='bootstrap3.darkly',
    list_layout='grid'
)
```

第三步，此时 `DJESite`的theme参数就可以指定你自定义的名称。

## 动态切换主题

根据用户的请求和设置为每一个请求指定特定的主题。以下是基于用户session设置切换主题。

```python
from django_echarts.starter.sites import DJESite
from django_echarts.core.themes import get_theme, Theme

class MySite(DJESite):
    
    def get_current_theme(self, request, *args, **kwargs):
        theme_name = request.session.get('theme')
        try:
            theme = get_theme(theme_name)
        except ValueError:
            theme = get_theme(self.theme)
        return theme
        
```



## 自定义UI框架

（此功能暂未实现.）

## 参考资料

- bootstrap3调色css: [ https://bootswatch.com/3/]( https://bootswatch.com/3/)
- materialcss: [https://materializecss.com/](https://materializecss.com/)