from functools import wraps
import inspect
from typing import Tuple


class ParameterMissingError(BaseException):
    pass


class LazyDict:
    """A dict support auto-resolve when get value."""

    def __init__(self):
        self._entries = {}
        self._opt_dic = {}
        self._dynamic_names = []
        self._dynamic_parameters = {}
        self._refs = {}  # dict[str,str]

    def func_register(self, obj, name: str = None, **kwargs):
        if not name and hasattr(obj, '__name__'):
            name = obj.__name__
        if not name:
            raise TypeError('The name must not be empty.')
        if callable(obj):
            self._dynamic_names.append(name)
            parameters = inspect.signature(obj).parameters
            if len(parameters) > 0:
                self._dynamic_parameters[name] = parameters
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
        """Set a alias name for the exist name."""
        self._refs[ref_name] = name
        return self

    def get(self, name: str, caller_kwargs: dict = None):
        if name in self._refs:
            name = self._refs[name]
        if name in self._entries:
            if name in self._dynamic_names:
                caller_kwargs = caller_kwargs or {}
                return self._entries[name](**caller_kwargs)
            else:
                return self._entries[name]
        return

    def actual_key(self, name):
        if name in self._refs:
            return self._refs[name]
        elif name in self._entries:
            return name
        return

    def keys(self):
        for k in self._entries.keys():
            yield k

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

    def validate_caller_params(self, func_name: str, param_dic: dict) -> Tuple[dict, bool]:
        """Validate and convert values with type annotation in registered function.
        """
        declare_dic = self._dynamic_parameters.get(func_name, None)
        is_parametric = declare_dic is not None
        if len(param_dic) == 0 or not is_parametric:
            return param_dic, is_parametric
        new_param_dic = {}
        extra_param_names = []
        for name, value in param_dic.items():
            if name in declare_dic:
                if declare_dic[name].annotation is not inspect.Parameter.empty:
                    new_val = declare_dic[name].annotation(value)  # Convert value
                    new_param_dic[name] = new_val
                else:
                    new_param_dic[name] = value
            else:
                extra_param_names.append(name)
        valid = False
        for name, parameter in declare_dic.items():
            if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                new_param_dic.update({k: v for k, v in param_dic.items()})
                valid = True
                break
            if parameter.default is not inspect.Parameter.empty and name not in param_dic:
                new_param_dic[name] = parameter.default
        if not valid and len(extra_param_names) == 0:
            valid = True
        if not valid:
            raise ParameterMissingError(f'These parameters are required: {",".join(extra_param_names)}')
        return new_param_dic, is_parametric

    def has_parameters(self, name: str) -> bool:
        name = self.actual_key(name)
        return name in self._dynamic_parameters

    def __contains__(self, item):
        return item in self._entries or item in self._refs

    def __len__(self):
        return len(self._entries)
