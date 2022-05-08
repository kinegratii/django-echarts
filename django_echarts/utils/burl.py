from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit


class BUrl:
    def __init__(self, url):
        self._url = url
        self._scheme, self._netloc, self._path, self._query_string, self._fragment = urlsplit(url)
        self._query_params = parse_qs(self._query_string)

    def replace(self, name, value, only_replace=False):
        if name not in self._query_params:
            if only_replace:
                return self
            self._query_params[name] = []
        self._query_params[name] = [value]
        return self

    def append(self, name, value):
        if name not in self._query_params:
            self._query_params[name] = []
        self._query_params[name].append(value)
        return self

    def delete(self, name):
        if name in self._query_params:
            del self._query_params[name]
        return self

    @property
    def url(self):
        new_query_string = urlencode(self._query_params, doseq=True)
        return urlunsplit((self._scheme, self._netloc, self._path, new_query_string, self._fragment))


def burl_args(url, *args):
    """Add query parameters to url.
    burl_args('/foo/', 'p', 1, 'q', 'test')  => '/foo/?p=1&q=test'
    """
    b = BUrl(url)
    _key = ''
    for i, value in enumerate(args):
        if i % 2 == 0:
            _key = value
        else:
            if _key and value is not None:
                b.replace(_key, value)
    return b.url


def burl_kwargs(url, **kwargs):
    b = BUrl(url)
    for k, v in kwargs.items():
        b.replace(k, v)
    return b.url
