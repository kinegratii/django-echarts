import uuid
from datetime import date

from typing import List, Union, Literal, Any

from borax.datasets.fetch import fetch

# TODO Move out of starter module.

__all__ = ['LinkItem', 'Menu', 'Jumbotron', 'Nav', 'Copyright', 'Message', 'ValuesPanel']


def _new_slug() -> str:
    return uuid.uuid4().hex


class LinkItem:
    """The data for the <a> element."""

    def __init__(self, text: str, url: str = None, slug: str = None,
                 new_page: bool = False, after_separator: bool = False):
        self.text = text
        self.url = url
        self.slug = slug or _new_slug()
        self.new_page = new_page
        self.after_separator = after_separator


class Menu:
    """The menu element in top nav."""
    __slots__ = ['text', 'slug', 'url', 'children']

    def __init__(self, text: str, slug: str = None, url: str = None):
        self.text = text
        self.slug = slug or _new_slug()
        self.url = url
        self.children = []  # type: List[LinkItem]


class Nav:
    def __init__(self):
        self.menus = []  # type: List[Menu]
        self.links = []  # type: List[LinkItem]

    def add_menu(self, text: str, slug: str = None, url: str = None):
        texts, slugs = fetch(self.menus, 'text', 'slug')
        if text in texts:
            return self
        if not slug or slug not in slugs:
            self.menus.append(Menu(text, slug, url))
        return self

    def add_item(self, menu_text: str, item: Union[LinkItem], after_separator=False):
        item.after_separator = after_separator
        for menu in self.menus:
            if menu.text == menu_text:
                menu.children.append(item)
                break
        return self

    def add_right_link(self, item: LinkItem):
        self.links.append(item)
        return self


class Jumbotron:
    """The main panel in home page."""
    __slots__ = ['title', 'main_text', 'small_text']

    def __init__(self, title: str, main_text: str, small_text: str):
        self.title = title
        self.main_text = main_text
        self.small_text = small_text


class Copyright:
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


class Message:
    __slots__ = ['text', 'title', 'catalog']

    def __init__(self, text, title: str = '提示', catalog: str = 'default'):
        self.text = text
        self.title = title
        self.catalog = catalog


def table_css(border=False, borderless=False, striped=False, size=None):
    class_list = ['table', 'table-responsive']
    if border:
        class_list.append('table-bordered')
    if borderless:
        class_list.append('table-borderless')
    if striped:
        class_list.append('table-striped')
    if size:
        class_list.append(f'table-{size}')
    return ' '.join(class_list)


class ValueItem:
    __slots__ = ['value', 'description', 'unit', 'catalog', 'arrow']

    def __init__(self, value: Any, description: str, unit: str = None, catalog: str = 'primary',
                 arrow: Literal['up', 'down', ''] = ''):
        self.value = str(value)
        self.description = description
        self.unit = unit or ''
        self.catalog = catalog
        self.arrow = arrow


class ValuesPanel:
    def __init__(self, col_item_num: int = 1):
        self._items = []  # type: List[ValueItem]
        self.col_item_num = col_item_num

    def add(self, value: Any, description: str, unit: str = None, catalog: str = 'primary',
            arrow: Literal['up', 'down', ''] = ''):
        item = ValueItem(value=value, description=description, unit=unit, catalog=catalog, arrow=arrow)
        self._items.append(item)
        return self

    def __iter__(self):
        yield from self._items
