# coding=utf8

"""
fetch is the way to fetch some field values to it own list;
"""

import operator
from itertools import tee


class Empty(object):
    pass


EMPTY = Empty()


def ifetch_single(iterable, key, default=EMPTY):
    attrgetter = operator.attrgetter(key)
    itemgetter = operator.itemgetter(key)

    def getter(item):
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

    return map(getter, iterable)


def fetch_single(iterable, key, default=EMPTY):
    return list(ifetch_single(iterable, key, default))


def ifetch_multiple(iterable, defaults, *keys):
    if len(keys) > 1:
        iters = tee(iterable, len(keys))
    else:
        iters = (iterable,)
    iters = [ifetch_single(it, key, default=defaults.get(key, EMPTY)) for it, key in zip(iters, keys)]
    return iters


def ifetch(iterable, key, *keys, **kwargs):
    """Iterator version of fetch()."""
    if len(keys) > 0:
        defaults = kwargs.pop('defaults', {})
        return map(list, ifetch_multiple(iterable, defaults, key, *keys))
    else:
        default = kwargs.pop('default', EMPTY)
        return ifetch_single(iterable, key, default=default)


def fetch(iterable, *keys, **kwargs):
    return list(ifetch(iterable, *keys, **kwargs))
