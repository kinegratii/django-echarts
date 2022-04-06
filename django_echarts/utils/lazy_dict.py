from functools import wraps


class LazyDict:
    """A dict support auto-resolve when get value."""

    def __init__(self):
        self._entries = {}
        self._opt_dic = {}
        self._dynamic_names = []
        self._refs = {}  # dict[str,str]

    def func_register(self, obj, name: str = None, **kwargs):
        if not name and hasattr(obj, '__name__'):
            name = obj.__name__
        if not name:
            raise TypeError('The name must not be empty.')
        if callable(obj):
            self._dynamic_names.append(name)
        self._entries[name] = obj
        self._opt_dic[name] = kwargs
        return self

    def register(self, function=None, name: str = None, **kwargs):
        def decorator(func):
            if not name and hasattr(func, '__name__'):
                cname = func.__name__
            else:
                cname = name
            self.func_register(func, cname, **kwargs)
            return func

        if function is None:
            return decorator
        else:
            return decorator(function)

    def set_ref(self, ref_name: str, name: str):
        self._refs[ref_name] = name
        return self

    def get(self, name: str):
        if name in self._refs:
            name = self._refs[name]
        if name in self._entries:
            if name in self._dynamic_names:
                return self._entries[name]()
            else:
                return self._entries[name]
        return

    def actual_key(self, name):
        if name in self._refs:
            return self._refs[name]
        elif name in self._entries:
            return name
        return

    def items(self):
        for k in self._entries.keys():
            yield k, self.get(k)

    def inject(self, *deps):

        def _inner(func):
            @wraps(func)
            def decorated(*args, **kwargs):
                kvs = {k: v for k, v in self.items() if k in deps}
                new_kwargs = {**kwargs, **kvs}
                return func(*args, **new_kwargs)

            return decorated

        return _inner

    def __contains__(self, item):
        return item in self._entries or item in self._refs

    def __len__(self):
        return len(self._entries)
