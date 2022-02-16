import copy
from typing import Dict

__all__ = ['Theme', 'ThemeManager', 'get_theme', 'install_theme']

_ORDERED_FIELDS_ = ['base_css', 'main_css', 'palette_css', 'font_css', 'jquery_js', 'main_js']
_EXTRA_FIELDS = ['cns']


def _parse_theme_label(label: str):
    """Parse theme label
    Labels:
        bootstrap5
        bootstrap5.cerulean
        bootstrap5:local
        bootstrap5.cerulean#local
    """
    if label.endswith('#local'):
        is_local = True
        label = label[:-6]
    else:
        is_local = False
    sl = label.split('.')
    if len(sl) < 2:
        theme, palette = sl[0], ''
    else:
        theme, palette = sl[:2]
    return label, theme, palette, is_local


class Theme:
    __slots__ = ['theme', 'name', 'theme_palette', 'js_urls', 'css_urls', 'cns', 'palette_css_url']

    def __init__(self, theme, theme_palette):
        self.theme = theme
        self.name = theme  # 'bootstrap3'
        self.theme_palette = theme_palette  # 'bootstrap3.yeti'
        self.js_urls = []
        self.css_urls = []
        self.cns = {}
        self.palette_css_url = ''

    def add_js(self, url: str):
        self.js_urls.append(url)

    def add_css(self, url: str):
        self.css_urls.append(url)

    def set_cns(self, cns):
        self.cns.update(cns)

    def iter_local_paths(self):
        items = []
        for url in self.css_urls + self.js_urls:
            if url == self.palette_css_url:
                local_path = '/'.join([self.name, self.theme_palette]) + '.min.css'
            else:
                filepath = url.rsplit('/')[-1]
                local_path = self.name + '/' + filepath
            items.append([url, local_path])
        return items

    def _localize_url(self, url: str, as_url=False):
        if url == self.palette_css_url:
            local_path = '/'.join([self.name, self.theme_palette]) + '.min.css'
        else:
            filepath = url.rsplit('/')[-1]
            local_path = self.name + '/' + filepath
        if as_url:
            local_path = '/static/' + local_path
        return url, local_path

    def local_theme(self) -> 'Theme':
        new_theme = Theme(self.theme, self.theme_palette)
        new_theme.cns = self.cns
        new_theme.js_urls = [self._localize_url(url, True)[1] for url in self.js_urls]
        new_theme.css_urls = [self._localize_url(url, True)[1] for url in self.css_urls]
        return new_theme

    def list_staticfiles(self):
        yield from self.css_urls
        yield from self.js_urls

    @classmethod
    def create_empty(cls, theme, theme_palette):
        return cls(theme, theme_palette)


_BUILTIN_FILE_CONFIG_ = {
    'bootstrap3': {
        'main_css': '',
        'palette_css': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
        'cns': {'row': 'row', 'col': 'col-md-{n}'}
    },
    'bootstrap5': {
        'palette_css': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css',
        'font_css': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js',
        'cns': {'row': 'row', 'col': 'col-sm-12 col-md-{n}'}  # n: the number of grids
    },
    'material': {
        'base_css': 'https://fonts.font.im/icon?family=Material+Icons',
        'palette_css': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css',
        'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js',
        'cns': {'row': 'row', 'col': 'col s12 m{n}'}
    }
}


class BuiltinRepoUtils:
    BOOTSTRAP3_PALETTES = [
        "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "lumen", "paper",
        "readable", "sandstone", "simplex", "slate", "spacelab", "superhero", "united", "yeti",
    ]
    BOOTSTRAP5_PALETTES = [
        "cerulea", "cosm", "cybor", "darkl", "flatl", "journa", "liter", "lume", "lu", "materi",
        "mint", "morp", "puls", "quart", "sandston", "simple", "sketch", "slat", "sola", "spacela",
        "superher", "unite", "vapo", "yet", "zephy",
    ]

    @staticmethod
    def is_bootstrap_palette(theme, palette):
        return (theme == 'bootstrap3' and palette in BuiltinRepoUtils.BOOTSTRAP3_PALETTES) or (
                    theme == 'bootstrap5' and palette in BuiltinRepoUtils.BOOTSTRAP5_PALETTES)

    @staticmethod
    def bootstrap_palette_css_url(theme, palette):
        version = theme[-1]
        return f'https://bootswatch.com/{version}/{palette}/bootstrap.min.css'


class ThemeManager:
    def __init__(self):
        self._data = copy.copy(_BUILTIN_FILE_CONFIG_)
        self._theme_dict = {}  # type: Dict[str,Theme]

    def install_themes(self, themes_config: dict) -> 'ThemeManager':
        for key, value in themes_config.items():
            if not isinstance(value, dict):
                continue
            if key in self._data:
                self._data[key].update(value)
            else:
                self._data[key] = value
        return self

    def install_theme(self, label: str, theme_config: dict):
        if label in self._data:
            self._data[label].update(theme_config)
        else:
            self._data[label] = theme_config
        return self

    def _build_theme(self, label: str) -> Theme:
        theme_palette, theme_name, palette, is_local = _parse_theme_label(label)
        is_bootstrap_palette = BuiltinRepoUtils.is_bootstrap_palette(theme_name, palette)
        if not (theme_palette in self._data or is_bootstrap_palette):
            raise ValueError(f'Unknown theme {theme_palette}. Choices are: {", ".join(self._data.keys())}')
        theme_obj = Theme.create_empty(theme_name, theme_palette)
        for f in _ORDERED_FIELDS_ + _EXTRA_FIELDS:
            val = self._data.get(theme_palette, {}).get(f, '')
            if not val:
                if is_bootstrap_palette and f == 'palette_css':
                    val = BuiltinRepoUtils.bootstrap_palette_css_url(theme_name, palette)
                else:
                    val = self._data.get(theme_name, {}).get(f, '')
            if not val:
                continue
            if f == 'cns':
                theme_obj.set_cns(val)
            if f.endswith('_js'):
                theme_obj.add_js(val)
            elif f.endswith('_css'):
                theme_obj.add_css(val)
                if f == 'palette_css':
                    theme_obj.palette_css_url = val
        if is_local:
            return theme_obj.local_theme()
        else:
            return theme_obj

    def get_theme(self, label: str) -> Theme:
        if label in self._theme_dict:
            return self._theme_dict[label]
        else:
            theme = self._build_theme(label)
            self._theme_dict[label] = theme
            return theme


_DEFAULT_THEME_MANAGER_ = ThemeManager()


def install_theme(label: str, theme_config: dict):
    """Add custom themes."""
    _DEFAULT_THEME_MANAGER_.install_theme(label, theme_config)


def get_theme(label: str) -> Theme:
    """Get a theme object from the default store.
    Labels:
        bootstrap5
        bootstrap5.cerulean
        bootstrap5:local
        bootstrap5.cerulean:local
    """
    return _DEFAULT_THEME_MANAGER_.get_theme(label)
