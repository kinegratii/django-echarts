from dataclasses import dataclass, field
from typing import Optional, List

from django import forms
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from typing_extensions import Literal


@dataclass
class SiteOpts:
    """The opts for DJESite."""
    list_layout: Literal['grid', 'list'] = 'grid'
    paginate_by: Optional[int] = 0
    nav_top_fixed: bool = False
    detail_tags_position: Literal['none', 'top', 'bottom'] = 'top'
    detail_sidebar_shown: bool = True
    nav_shown_pages: List = field(default_factory=lambda: ['home'])


page_num_choices = ((0, '不分页'), (5, '5'), (10, '10'), (15, '15'), (20, '20'))
bool_choices = ((True, 'Yes'), (False, 'No'))


class SiteOptsForm(forms.Form):
    nav_top_fixed = forms.TypedChoiceField(label='是否固定顶部导航栏', coerce=lambda x: x == 'True', choices=bool_choices)
    list_layout = forms.ChoiceField(label='列表页布局', choices=(('list', '列表布局'), ('grid', '网格布局')))
    paginate_by = forms.TypedChoiceField(label='每页项目数', coerce=int, initial=0, choices=page_num_choices)
    theme_palette_name = forms.ChoiceField(label='主题调色')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(k, k) for k in DJANGO_ECHARTS_SETTINGS.theme_manger.available_palettes]
        self.fields['theme_palette_name'].choices = choices
