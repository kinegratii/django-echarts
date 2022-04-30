# 第三方HTML渲染库 

本文介绍了一些常用的 HTML渲染库。

## htmlgenerator

地址： [https://github.com/basxsoftwareassociation/htmlgenerator](https://github.com/basxsoftwareassociation/htmlgenerator)

### 安装

自 v0.5.2开始，django-echarts 已经内置 htmlgenerator 作为依赖库，无需额外安装。

### 创建元素

下面是一个简单的例子。

```python
import htmlgenerator as hg

my_page = hg.HTML(hg.HEAD(), hg.BODY(hg.H1("It works!")))
print(hg.render(my_page, {}))

my_element = hg.DIV('This is a text.', _class='panel', id='my-div')
print(hg.render(my_element, {}))
```

说明：

1. 在 htmlgenerator中，所有元素均是 `htmlgenerator.BaseElement` 的子类。
2. HTML标签以大写字符串
3. 子节点以位置参数传入
4. 属性值以关键字参数传入

### 动态值

使用 `htmlgenerator.render` 函数可以对同一元素进行多次不同渲染。

```python
my_div = hg.DIV("Hello, ", hg.C("person.name"))

print(hg.render(my_div, {"person": {"name": "Alice", "occupation": "Writer"}},))

print(hg.render(my_div,{"person": {"name": "John", "occupation": "Police"}},))
```

### Django页面响应对象

`BaseElement` 类的 `render` 函数返回值可以直接传入 `HttpResponse`。

```python
from django.http import HttpResponse

def render_layout_to_response(request, layout, context):
    return HttpResponse(layout.render(context))
```



### 与django-echarts

django-echarts 渲染模块内置支持 `htmlgenerator.BaseElement`  类型。因此

- 可以作为模板标签函数 `dw_widget` 的参数 
- 可以作为 `Container.add_widget` 的参数，融入现有的组件体系



```python
import htmlgenerator as hg
from django_echarts.entities import RowContainer

container = RowContainer()
header_div = hg.DIV(hg.H1('Page Title'), _class='header')
container.add_widget(header_div)
```

