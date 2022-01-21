import uuid
from typing import List, Union

from borax.datasets.fetch import fetch

__all__ = ['LinkItem', 'Menu', 'Jumbotron', 'Nav']


def _new_slug() -> str:
    return uuid.uuid4().hex


class LinkItem:
    __slots__ = ['title', 'url', 'slug', 'new_page', 'after_separator']

    def __init__(self, title: str, url: str = None, slug: str = None,
                 new_page: bool = False, after_separator: bool = False):
        self.title = title
        self.url = url
        self.slug = slug or _new_slug()
        self.new_page = new_page
        self.after_separator = after_separator


class Menu:
    __slots__ = ['title', 'slug', 'url', 'children']

    def __init__(self, title: str, slug: str = None, url: str = None):
        self.title = title
        self.slug = slug or _new_slug()
        self.url = url
        self.children = []  # type: List[LinkItem]


class Nav:
    def __init__(self):
        self.menus = []  # type: List[Menu]
        self.links = []  # type: List[LinkItem]

    def add_menu(self, title: str, slug: str = None, url: str = None):
        titles, slugs = fetch(self.menus, 'title', 'slug')
        if title in titles:
            return self
        if not slug or slug not in slugs:
            self.menus.append(Menu(title, slug, url))
        return self

    def add_item(self, menu_title: str, item: Union[LinkItem], after_separator=False):
        item.after_separator = after_separator
        for menu in self.menus:
            if menu.title == menu_title:
                menu.children.append(item)
                break
        return self

    def add_right_link(self, item: LinkItem):
        self.links.append(item)
        return self


class Jumbotron:
    __slots__ = ['title', 'main_text', 'small_text']

    def __init__(self, title: str, main_text: str, small_text: str):
        self.title = title
        self.main_text = main_text
        self.small_text = small_text
