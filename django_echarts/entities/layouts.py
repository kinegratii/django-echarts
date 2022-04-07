import re
from functools import singledispatch
from typing import List, Union

__all__ = ['LayoutOpts', 'TYPE_LAYOUT_OPTS', 'any2layout']

_defaults = {'l': 8, 'r': 8, 's': 8, 't': 6, 'b': 6, 'f': 12}

_rm = re.compile(r'([lrtbfsa])(([1-9]|(1[12]))?)')


class LayoutOpts:
    """Layout for user defined.
    """
    __slots__ = ['pos', 'spans', 'start']

    # l=left,r=right,s=stripped,t=top,b=bottom,f=full
    _defaults = {'l': 8, 'r': 8, 's': 8, 't': 6, 'b': 6, 'f': 12}

    _rm = re.compile(r'([lrtbfsa])(([1-9]|(1[12]))?)')

    def __init__(self, pos: str = 'r', spans: List[int] = None):
        self.pos = pos
        self.spans = spans or []
        self.start = pos in 'rb'

    def stripped_layout(self) -> 'LayoutOpts':
        if self.pos == 'r':
            return LayoutOpts(pos='l', spans=self.spans)
        elif self.pos == 'l':
            return LayoutOpts(pos='r', spans=self.spans)
        else:
            return self

    def __str__(self):
        return f'<LOptions:{self.pos},{self.spans}>'


TYPE_LAYOUT_OPTS = Union[int, List[int], str]


@singledispatch
def any2layout(obj) -> LayoutOpts:
    raise TypeError('Can not parse LayOpts.')


@any2layout.register(LayoutOpts)
def _(obj) -> LayoutOpts:
    return obj


@any2layout.register(int)
def _(obj) -> LayoutOpts:
    return LayoutOpts(spans=[obj])


@any2layout.register(list)
def _(obj) -> LayoutOpts:
    return LayoutOpts(spans=obj)


@any2layout.register(str)
def _(obj) -> LayoutOpts:
    m = _rm.match(obj)
    if m:
        pos, cols = m.group(1), m.group(2)
        if cols is None or cols == '':
            cols = _defaults.get(pos, 8)
        else:
            cols = int(cols)
        return LayoutOpts(pos, [cols])
    else:
        raise ValueError(f'This layout can not be parsed: {obj}')
