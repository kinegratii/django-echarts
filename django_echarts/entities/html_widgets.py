import uuid
import warnings
from datetime import date
from typing import List, Union, Any

from borax.datasets.fetch import fetch
from borax.htmls import html_tag
from typing_extensions import Literal

from .containers import RowContainer

__all__ = ['LinkItem', 'SeparatorItem', 'Menu', 'Jumbotron', 'Nav', 'Copyright', 'Message', 'ValuesPanel', 'ValueItem']


def _new_slug() -> str:
    return uuid.uuid4().hex


class HTMLBase:
    """A entity class for html widget without any js_dependencies."""
    pass


class LinkItem(HTMLBase):
    """The data for the <a> element."""

    def __init__(self, text: str, url: str = None, slug: str = None,
                 new_page: bool = False, after_separator: bool = False):
        self.text = text
        self.url = url
        self.slug = slug or _new_slug()
        self.new_page = new_page
        self.after_separator = after_separator


class SeparatorItem(HTMLBase):
    pass


class Menu(HTMLBase):
    """The menu element in top nav."""
    __slots__ = ['text', 'slug', 'url', 'children']

    def __init__(self, text: str, slug: str = None, url: str = None):
        self.text = text
        self.slug = slug or _new_slug()
        self.url = url
        self.children = []  # type: List[LinkItem]


class Nav:
    """A html widget for top nav and footer links."""
    CHART_PLACEHOLDER = 'chart_nav'  # A placeholder for chart nav.

    def __init__(self):
        self.left_menus = []  # type: List[Menu]
        self.right_menus = []  # type:List[Menu]
        self.footer_links = []  # type: List[LinkItem]

    @property
    def menus(self):
        return self.left_menus

    @property
    def links(self):
        return self.right_menus

    def add_left_menu(self, text: str, slug: str = None, url: str = None):
        texts, slugs = fetch(self.left_menus, 'text', 'slug')
        if text in texts:
            return self
        if not slug or slug not in slugs:
            self.left_menus.append(Menu(text, slug, url))
        return self

    def add_right_menu(self, text: str, slug: str = None, url: str = None):
        texts, slugs = fetch(self.right_menus, 'text', 'slug')
        if text in texts:
            return self
        if not slug or slug not in slugs:
            self.right_menus.append(Menu(text, slug, url))
        return self

    def add_item_in_left_menu(self, menu_text: str, item: Union[LinkItem], after_separator=False):
        item.after_separator = item.after_separator | after_separator
        for menu in self.left_menus:
            if menu.text == menu_text:
                menu.children.append(item)
                break
        return self

    def add_item_in_right_menu(self, menu_text: str, item: Union[LinkItem], after_separator=False):
        item.after_separator = item.after_separator | after_separator
        for menu in self.left_menus:
            if menu.text == menu_text:
                menu.children.append(item)
                break
        return self


class LinkGroup(HTMLBase):
    """A list panel containing links."""
    widget_type = 'LinkGroup'

    def __init__(self):
        self.widgets = []  # type:List[LinkItem]

    def add_widget(self, widget: LinkItem):
        self.widgets.append(widget)

    def __iter__(self):
        for widget in self.widgets:
            yield widget


class Jumbotron(HTMLBase):
    widget_type = 'Jumbotron'
    """The main panel in home page."""
    __slots__ = ['title', 'main_text', 'small_text']

    def __init__(self, title: str, main_text: str, small_text: str):
        self.title = title
        self.main_text = main_text
        self.small_text = small_text


class Copyright(HTMLBase):
    widget_type = 'Copyright'
    """The copyright text on the footer in every page."""
    __slots__ = ['year_range', 'powered_by']

    def __init__(self, start_year: int, powered_by: str):
        this_year = date.today().year
        self.year_range = f'{start_year}-{this_year}'
        self.powered_by = powered_by


class ThemeColor:
    DEFAULT = 'default'
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    DANGER = 'danger'
    WARNING = 'warning'
    INFO = 'info'
    LIGHT = 'light'
    DARK = 'dark'


class Message(HTMLBase):
    widget_type = 'Message'
    __slots__ = ['text', 'title', 'catalog']

    def __init__(self, text, title: str = '提示', catalog: str = 'default'):
        self.text = text
        self.title = title
        self.catalog = catalog


class ValueItem(HTMLBase):
    __slots__ = ['value', 'description', 'unit', 'catalog', 'arrow']

    def __init__(self, value: Any, description: str, unit: str = None, catalog: str = 'primary',
                 arrow: Literal['up', 'down', ''] = ''):
        self.value = str(value)
        self.description = description
        self.unit = unit or ''
        self.catalog = catalog
        self.arrow = arrow


class ValuesPanel(RowContainer):
    """A row container containing some ValueItem objects.
    This class is not recommend anymore, use RowContainer instead.
    """

    def __init__(self, col_item_num: int = 1):
        warnings.warn('This class is deprecated.Use RowContainer instead.', PendingDeprecationWarning, stacklevel=2)
        super(ValuesPanel, self).__init__()
        self.col_item_num = col_item_num

    def add(self, value: Any, description: str, unit: str = None, catalog: str = 'primary',
            arrow: Literal['up', 'down', ''] = ''):
        warnings.warn('This method is deprecated.Use ValuesPanel.add_widget instead.', DeprecationWarning, stacklevel=2)
        item = ValueItem(value=value, description=description, unit=unit, catalog=catalog, arrow=arrow)
        self.add_widget(item)
        return self


class Title(HTMLBase):
    __slots__ = ['text', 'small_text']

    def __init__(self, text: str, small_text: str = None):
        self.text = text
        self.small_text = small_text


class ElementEntity(HTMLBase):
    """A common entity for a html element."""

    def __init__(self, tag_name: str, id_: str = None, content: str = None, class_: str = None, style: dict = None,
                 style_width: str = None, style_height: str = None, **kwargs):
        self.tag_name = tag_name
        self.id_ = id_
        self.class_ = class_
        self.content = content
        self.style = style or {}
        if style_width is not None:
            self.style.update({'width': style_width})
        if style_height is not None:
            self.style.update({'height': style_height})
        self.style = {k: v for k, v in self.style.items() if v not in (None, '', [], ())}
        self.attrs = kwargs

    def __html__(self):
        return html_tag(self.tag_name, id_=self.id_, content=self.content, class_=self.class_, style=self.style,
                        **self.attrs)
