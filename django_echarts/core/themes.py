import copy

__all__ = ['Theme', 'ThemeManager', 'get_theme', 'install_themes']

_ORDERED_FIELDS_ = ['base_css', 'main_css', 'palette_css', 'jquery_js', 'main_js']


class Theme:
    __slots__ = ['theme', 'name', 'theme_palette', 'js_urls', 'css_urls']

    def __init__(self, theme, theme_palette, js_urls, css_urls):
        self.theme = theme
        self.name = theme
        self.theme_palette = theme_palette
        self.js_urls = js_urls
        self.css_urls = css_urls


_BUILTIN_FILE_URLS = {
    'bootstrap3': {
        'main_css': '',
        'palette_css': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js'
    },
    'bootstrap3.cerulean': {
        'palette_css': '/static/bootstrap3/bootstrap3.cerulean.min.css'
    },
    'material': {
        'base_css': 'https://fonts.font.im/icon?family=Material+Icons',
        'palette_css': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js'
    }
}


class ThemeManager:
    def __init__(self):
        self._data = copy.copy(_BUILTIN_FILE_URLS)

    def install_themes(self, themes_config: dict) -> 'ThemeManager':
        for key, value in themes_config.items():
            if not isinstance(value, dict):
                continue
            if key in self._data:
                self._data[key].update(value)
            else:
                self._data[key] = value
        return self

    def get_theme(self, label: str) -> Theme:
        theme = label.split('.')[0]
        theme_palette = label
        if theme_palette not in self._data:
            raise ValueError(f'Unknown theme {theme_palette}. Choices are: {", ".join(self._data.keys())}')
        js_urls, css_urls = [], []
        for f in _ORDERED_FIELDS_:
            url = self._data.get(theme_palette, {}).get(f, '')
            if not url:
                url = self._data.get(theme, {}).get(f, '')
            if not url:
                continue
            if f.endswith('_js'):
                js_urls.append(url)
            elif f.endswith('_css'):
                css_urls.append(url)
        return Theme(theme, theme_palette, js_urls, css_urls)


_DEFAULT_THEME_MANAGER_ = ThemeManager()


def install_themes(themes_config: dict):
    """Add custom themes."""
    _DEFAULT_THEME_MANAGER_.install_themes(themes_config)


def get_theme(label: str) -> Theme:
    """Get a theme object from the default store."""
    return _DEFAULT_THEME_MANAGER_.get_theme(label)
