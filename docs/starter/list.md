

# 列表页面（List）

列表页面按照列表方式显示了所有图表的基本信息，默认实现类 `DJESiteListView` 。

## 设置分页

有两种方式设置，第一种在site创建时传入 `paginate_by` 参数，指定每页需要显示的数目，默认不启用分页特性。

```python
site_obj = DJESite(
    site_title='图表可视化',
    paginate_by=10
)
```

第二种，如果需要替换默认的模板文件，继承 `DJESiteListView`，重新指定 paginator_template_name 即可。

```python
class MyListListView(DJESiteListView):
    paginator_template_name = 'my_paginator_list.html'
    paginate_by = 15

site_obj.register_list_view(MyListListView)
```

需要注意的是，MyListListView中paginate_by值将覆盖site初始化传入的值，比如上述两个片段整合时paginate_by即为15。

## 模板API

根据是否具有分页特性，使用不同的模板文件，并传入不同模板变量。

| 特性   | 模板                             | 变量名称         | 类型                         | 说明                                     |
| ------ | -------------------------------- | ---------------- | ---------------------------- | ---------------------------------------- |
| 无分页 | {theme}/list.html                | chart_list       | `List[DJEChartInfo]`         | 图表的基本信息，包括标题、标识、介绍文本 |
| 有分页 | {theme}/list_with_paginator.html | page_obj         | `django.core.paginator.Page` | django构建的分页对象。                   |
|        |                                  | elided_page_nums | List[Union[int, str]]        | 页码列举。仅在Django3.2+有效。           |

备注：

- 其中page_obj.object_list 是具体的条目数据，类型与chart_list相关，其他属性可以参见 [《Django Paginator 》](https://docs.djangoproject.com/en/4.0/topics/pagination/)。

