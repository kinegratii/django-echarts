# coding=utf8

"""
fetch is the way to fetch some field values to it own list;
"""

import operator
from itertools import tee
from functools import partial


class Empty(object):
    pass


EMPTY = Empty()


def ifetch_single(iterable, key, default=EMPTY, getter=None):
    """
    getter() g(item, key):pass
    """

    def _getter(item):
        if getter:
            return partial(getter, key=key)(item)
        else:
            attrgetter = operator.attrgetter(key)
            itemgetter = operator.itemgetter(key)
            try:
                return attrgetter(item)
            except AttributeError:
                pass

            try:
                return itemgetter(item)
            except KeyError:
                pass

        if default is not EMPTY:
            return default

        raise ValueError('Item %r has no attr or key for %r' % (item, key))

    return map(_getter, iterable)


def fetch_single(iterable, key, default=EMPTY, getter=None):
    return list(ifetch_single(iterable, key, default=default, getter=getter))


def ifetch_multiple(iterable, defaults, getter=None, *keys):
    if len(keys) > 1:
        iters = tee(iterable, len(keys))
    else:
        iters = (iterable,)
    iters = [ifetch_single(it, key, default=defaults.get(key, EMPTY), getter=getter) for it, key in zip(iters, keys)]
    return iters


def ifetch(iterable, key, *keys, **kwargs):
    """Iterator version of fetch()."""
    if len(keys) > 0:
        defaults = kwargs.pop('defaults', {})
        getter = kwargs.pop('getter', None)
        return map(list, ifetch_multiple(iterable, defaults, getter, key, *keys))
    else:
        default = kwargs.pop('default', EMPTY)
        getter = kwargs.pop('getter', None)
        return ifetch_single(iterable, key, default=default, getter=getter)


def fetch(iterable, *keys, **kwargs):
    return list(ifetch(iterable, *keys, **kwargs))
