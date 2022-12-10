class EntityURI:
    __empty = None

    CATALOG_CHART = 'chart'
    CATALOG_INFO = 'info'
    CATALOG_WIDGET = 'widget'
    CATALOG_LAYOUT = 'layout'
    CATALOG_COLLECTION = 'collection'

    __slots__ = ['catalog', 'name', 'params', '_params_path']

    def __init__(self, catalog: str, name: str, params: dict = None):
        self.catalog = catalog
        self.name = name
        self.params = params or {}
        self._params_path = '/'.join([item for kv in self.params.items() for item in kv])

    @property
    def params_path(self):
        return self._params_path

    def __str__(self):
        return f'{self.catalog}:{self.name}'

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
