# coding=utf8
"""
fetch is a enhance module with fetch. And adjust the parameter order of calling to fit the habit.
"""
import operator
from itertools import tee
from functools import partial

__all__ = ['fetch', 'ifetch', 'fetch_single', 'ifetch_multiple', 'ifetch_single']


class Empty(object):
    pass


EMPTY = Empty()


def ifetch_single(iterable, key, default=EMPTY, getter=None):
    """
    getter() g(item, key):pass
    """

    def _getter(item):
        if getter:
            custom_getter = partial(getter, key=key)
            return custom_getter(item)
        else:
            try:
                attrgetter = operator.attrgetter(key)
                return attrgetter(item)
            except AttributeError:
                pass

            try:
                itemgetter = operator.itemgetter(key)
                return itemgetter(item)
            except KeyError:
                pass

            if default is not EMPTY:
                return default

            raise ValueError('Item %r has no attr or key for %r' % (item, key))

    return map(_getter, iterable)


def fetch_single(iterable, key, default=EMPTY, getter=None):
    return list(ifetch_single(iterable, key, default=default, getter=getter))


def ifetch_multiple(iterable, *keys, defaults=None, getter=None):
    defaults = defaults or {}
    if len(keys) > 1:
        iters = tee(iterable, len(keys))
    else:
        iters = (iterable,)
    iters = [ifetch_single(it, key, default=defaults.get(key, EMPTY), getter=getter) for it, key in zip(iters, keys)]
    return iters


def ifetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None):
    if len(keys) > 0:
        keys = (key,) + keys
        return map(list, ifetch_multiple(iterable, *keys, defaults=defaults, getter=getter))
    else:
        return ifetch_single(iterable, key, default=default, getter=getter)


def fetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None):
    return list(ifetch(iterable, key, *keys, default=default, defaults=defaults, getter=getter))
