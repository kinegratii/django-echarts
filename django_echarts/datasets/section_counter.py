# coding=utf8
"""
A counter module for data count.
"""
from __future__ import unicode_literals

from collections import Counter

MIN_LOWER = -100000


class BIndex(object):
    def __contains__(self, item):
        return False

    def __str__(self):
        return '<Index>'

    def _key(self):
        return 0


class BValueIndex(BIndex):
    def __init__(self, value):
        self.value = value

    def __contains__(self, item):
        return item == self.value

    def __str__(self):
        return str(self.value)

    def _key(self):
        return self.value


class BRangeIndex(BIndex):
    def __init__(self, lower=None, upper=None):
        self.lower = lower
        self.upper = upper
        self._include_lower = self.lower is not None
        self._include_upper = self.upper is not None

    def __contains__(self, item):
        if self._include_lower:
            if self._include_upper:
                return self.lower <= item < self.upper
            else:
                return self.lower <= item
        else:
            if self._include_upper:
                return item < self.upper
            else:
                return True

    def __str__(self):
        if self._include_lower and self._include_upper:
            return '{0}~{1}'.format(self.lower, self.upper)
        elif self._include_lower:
            return '≥{}'.format(self.lower)
        elif self._include_upper:
            return '<{}'.format(self.upper)
        else:
            return '~'

    def _key(self):
        return self.lower if self._include_lower else MIN_LOWER


class BSectionCounter(object):
    def __init__(self, *indexes):
        self.indexes = indexes

    def feed(self, data):
        c = Counter()
        for d in data:
            c.update([r.__str__() for r in self.indexes if d in r])
        return c

    def feed_as_axises(self, data):
        pass

    def axis(self):
        pass

    @classmethod
    def from_simple(cls, *index_or_number_list):
        indexes = []
        for ion in index_or_number_list:
            if isinstance(ion, BIndex):
                indexes.append(ion)
            elif isinstance(ion, (tuple, list)) and len(ion) == 2:
                indexes.append(BRangeIndex(ion[0], ion[1]))
            else:
                indexes.append(BValueIndex(ion))
        return cls(*indexes)

    @classmethod
    def from_range(cls, start, end, step):
        indexes = [BRangeIndex(i, i + step) for i in range(start, end, step)]
        return cls(*indexes)
