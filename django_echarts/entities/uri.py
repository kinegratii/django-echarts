class EntityURI:
    CATALOG_CHART = 'chart'
    CATALOG_INFO = 'info'
    CATALOG_WIDGET = 'widget'
    CATALOG_LAYOUT = 'layout'
    CATALOG_COLLECTION = 'collection'

    __slots__ = ['catalog', 'name', 'params']

    def __init__(self, catalog: str, name: str, params: dict = None):
        self.catalog = catalog
        self.name = name
        self.params = params or {}

    @classmethod
    def from_params_path(cls, catalog: str, name: str, params_path: str):
        params = {}
        if params_path:
            kw = params_path.split('/')
            for i in range(0, len(kw), 2):
                params[kw[i]] = kw[i + 1]
        return cls(catalog, name, params)
