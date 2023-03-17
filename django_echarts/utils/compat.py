from django import VERSION as django_version
from django.core.paginator import Paginator


def compat_get_elided_page_range(paginator: Paginator, number=1, *, on_each_side=3, on_ends=2):
    if django_version > (3, 2):
        return paginator.get_elided_page_range(number, on_each_side=on_each_side, on_ends=on_ends)
    else:
        return _get_elided_page_range(paginator, number, on_each_side=on_each_side, on_ends=on_ends)


def _get_elided_page_range(paginator: Paginator, number=1, *, on_each_side=3, on_ends=2):
    """
    Return a 1-based range of pages with some values elided.

    If the page range is larger than a given size, the whole range is not
    provided and a compact form is returned instead, e.g. for a paginator
    with 50 pages, if page 43 were the current page, the output, with the
    default arguments, would be:

        1, 2, …, 40, 41, 42, 43, 44, 45, 46, …, 49, 50.
    """
    number = paginator.validate_number(number)

    if paginator.num_pages <= (on_each_side + on_ends) * 2:
        yield from paginator.page_range
        return

    if number > (1 + on_each_side + on_ends) + 1:
        yield from range(1, on_ends + 1)
        yield paginator.ELLIPSIS
        yield from range(number - on_each_side, number + 1)
    else:
        yield from range(1, number + 1)

    if number < (paginator.num_pages - on_each_side - on_ends) - 1:
        yield from range(number + 1, number + on_each_side + 1)
        yield paginator.ELLIPSIS
        yield from range(paginator.num_pages - on_ends + 1, paginator.num_pages + 1)
    else:
        yield from range(number + 1, paginator.num_pages + 1)
