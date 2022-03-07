from dataclasses import dataclass, field
from typing import Optional, List, Literal

from django import forms


@dataclass
class SiteOpts:
    """The opts for DJESite."""
    list_layout: Literal['grid', 'list'] = 'grid'
    paginate_by: Optional[int] = 0
    detail_tags_position: Literal['none', 'top', 'bottom'] = 'top'
    detail_sidebar_shown: bool = True
    nav_shown_pages: List = field(default_factory=lambda: ['home'])


page_num_choices = ((0, '不分页'), (5, '5'), (10, '10'), (15, '15'), (20, '20'))


class SiteOptsForm(forms.Form):
    list_layout = forms.ChoiceField(label='列表页布局', choices=(('list', '列表布局'), ('grid', '网格布局')))
    paginate_by = forms.TypedChoiceField(label='每页项目数', coerce=int, initial=0, choices=page_num_choices)
    theme_palette_name = forms.ChoiceField(label='主题调色')
