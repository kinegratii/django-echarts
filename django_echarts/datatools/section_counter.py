# coding=utf8
"""
A indexes-based counter module for value list.
1. It is some likely feature but indexes-based
2. Index match supports the "in" operator
3. The counter of missing index will be set to 0
4. export to counter or axis data list
"""

from collections import Counter

MIN_LOWER = -100000  # The min value of range lower.


class BIndex:
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


class BSectionIndex(BIndex):
    def __init__(self, lower=None, upper=None):
        self.lower = lower
        self.upper = upper
        self._lower_specified = self.lower is not None
        self._upper_specified = self.upper is not None

    def __contains__(self, item):
        if self._lower_specified:
            if self._upper_specified:
                return self.lower <= item <= self.upper
            else:
                return self.lower <= item
        else:
            if self._upper_specified:
                return item <= self.upper
            else:
                return True

    def __str__(self):
        if self._lower_specified and self._upper_specified:
            return '{0}~{1}'.format(self.lower, self.upper)
        elif self._lower_specified:
            return '≥{}'.format(self.lower)
        elif self._upper_specified:
            return '≤{}'.format(self.upper)
        else:
            return '~'

    def _key(self):
        return self.lower if self._lower_specified else MIN_LOWER


class BRangeIndex(BIndex):
    def __init__(self, lower=None, upper=None):
        self.lower = lower
        self.upper = upper
        self._lower_specified = self.lower is not None
        self._upper_specified = self.upper is not None

    def __contains__(self, item):
        if self._lower_specified:
            if self._upper_specified:
                return self.lower <= item < self.upper
            else:
                return self.lower <= item
        else:
            if self._upper_specified:
                return item < self.upper
            else:
                return True

    def __str__(self):
        if self._lower_specified and self._upper_specified:
            return '{0}~{1}'.format(self.lower, self.upper)
        elif self._lower_specified:
            return '≥{}'.format(self.lower)
        elif self._upper_specified:
            return '<{}'.format(self.upper)
        else:
            return '~'

    def _key(self):
        return self.lower if self._lower_specified else MIN_LOWER


class BSectionCounter:
    def __init__(self, *indexes):
        self.indexes = indexes

    def feed(self, data):
        c = Counter({str(r): 0 for r in self.indexes})
        for d in data:
            c.update([str(r) for r in self.indexes if d in r])
        return c

    def feed_as_axises(self, data):
        rc = self.feed(data)
        keys = sorted(self.indexes, key=lambda x: x._key())
        return zip(*[(str(k), rc[str(k)]) for k in keys])

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
