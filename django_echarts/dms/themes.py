__all__ = ['get_theme']

_ORDERED_FIELDS_ = ['base_css', 'main_css', 'palette_css', 'jquery_js', 'main_js']


class Theme:
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
        'main_css': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js'
    }
}


def get_theme(theme, theme_palette) -> Theme:
    if theme not in _BUILTIN_FILE_URLS and theme_palette not in _BUILTIN_FILE_URLS:
        raise ValueError(f'Unknown theme {theme_palette}. Choices are: {", ".join(_BUILTIN_FILE_URLS.keys())}')
    js_urls, css_urls = [], []
    for f in _ORDERED_FIELDS_:
        url = _BUILTIN_FILE_URLS.get(theme_palette, {}).get(f, '')
        if not url:
            url = _BUILTIN_FILE_URLS.get(theme, {}).get(f, '')
        if not url:
            continue
        if f.endswith('_js'):
            js_urls.append(url)
        elif f.endswith('_css'):
            css_urls.append(url)
    return Theme(theme, theme_palette, js_urls, css_urls)
