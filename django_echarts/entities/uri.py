from typing import List, Union, Generator
import itertools


class EntityURI:
    __empty = None

    CATALOG_CHART = 'chart'
    CATALOG_INFO = 'info'
    CATALOG_WIDGET = 'widget'
    CATALOG_LAYOUT = 'layout'
    CATALOG_COLLECTION = 'collection'

    CATALOG_VIEW = 'view'
    # TODO description attr

    __slots__ = ['catalog', 'name', 'params', '_params_path']

    def __init__(self, catalog: str, name: str, params: dict = None):
        self.catalog = catalog
        self.name = name
        self.params = params or {}
        _items = []
        for k, v in self.params.items():
            _items.extend([k, str(v)])
        self._params_path = '/'.join(_items)

    @property
    def params_path(self):
        return self._params_path

    def __str__(self):
        if len(self.params):
            return f'{self.catalog}:{self.name}/{self.params_path}'
        else:
            return f'{self.catalog}:{self.name}'

    __repr__ = __str__

    def is_empty(self):
        return not self.catalog or self.catalog == 'empty'

    @classmethod
    def empty(cls):
        if cls.__empty is None:
            cls.__empty = cls('empty', '')
        return cls.__empty

    @classmethod
    def from_params_path(cls, catalog: str, name: str, params_path: str, param_names: list = None):
        """Parse URI param string to  param dict.
        param_names is required when param value contains '/' character.
        """
        params = {}
        if not params_path:
            return cls(catalog, name, params)
        kw = params_path.split('/')
        if param_names:
            name2pos = []
            for pn in param_names:
                try:
                    pos = kw.index(pn)
                    name2pos.append((pn, pos))
                except IndexError:
                    pass
            name2pos.sort(key=lambda _item: _item[1])
            for i, item in enumerate(name2pos):
                pname, npos = item
                start_pos = npos + 1
                if i == len(name2pos) - 1:
                    end_pos = len(kw)
                else:
                    end_pos = name2pos[i + 1][1]
                if end_pos - start_pos == 1:
                    value = kw[start_pos]
                else:
                    value = '/'.join(kw[start_pos:end_pos])
                params[pname] = value
        else:
            for i in range(0, len(kw), 2):
                params[kw[i]] = kw[i + 1]
        return cls(catalog, name, params)

    @classmethod
    def from_str(cls, s: str, catalog: str = None, param_names: list = None):
        pos1 = s.find(':')
        if pos1 == -1:
            _catalog, st = catalog, s
        else:
            _catalog, st = s[:pos1], s[pos1 + 1:]
        if len(st) == 0:
            st = _catalog
            _catalog = catalog
        pos = st.find('/')
        if pos == -1:
            name, params_path = st, ''
        else:
            name, params_path = st[:pos], st[pos + 1:]
        return cls.from_params_path(_catalog, name, params_path, param_names)


USER_PARAMS_CONFIGS_TYPE = Union[List[dict], dict]


def parse_params_choices(config: USER_PARAMS_CONFIGS_TYPE) -> Generator[dict, None, None]:
    """
    [{'year':2021, 'month':1},{'year':2021, 'month':2},]
    {'year':[2021,2022], 'month':[1,2]}
    """
    if isinstance(config, List):
        for item in config:
            yield item
    else:
        names = []
        values_list = []
        for name, values in config.items():
            names.append(name)
            values_list.append(values)
        for t in itertools.product(*values_list):
            item = dict((k, v) for k, v in zip(names, t))
            yield item


class ParamsConfig:
    __empty__ = None
    __slots__ = ['choices']

    def __init__(self, choices: USER_PARAMS_CONFIGS_TYPE = None):
        self.choices = choices or []

    def __iter__(self):
        for param_dic in parse_params_choices(self.choices):
            yield param_dic

    @classmethod
    def empty(cls):
        if ParamsConfig.__empty__ is None:
            ParamsConfig.__empty__ = ParamsConfig()
        return ParamsConfig.__empty__
