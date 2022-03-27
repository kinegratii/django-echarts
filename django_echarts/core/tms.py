import importlib
from collections import OrderedDict
from typing import List, Dict

__all__ = ['Theme', 'parse_theme_label', 'ThemeManager']

_ORDERED_FIELDS_ = ['base_css', 'main_css', 'palette_css', 'font_css', 'jquery_js', 'main_js']
_EXTRA_FIELDS = ['cns']


def parse_theme_label(label: str):
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
    __slots__ = ['theme', 'name', 'theme_palette', 'cns', 'palette_css_url', '_url_dic', 'is_local']

    def __init__(self, theme, theme_palette, is_local: bool = False):
        self.theme = theme
        self.name = theme  # 'bootstrap3'
        self.theme_palette = theme_palette  # 'bootstrap3.yeti'

        self._url_dic = OrderedDict()
        self.cns = {}

        self.is_local = is_local
        self.palette_css_url = ''

    @property
    def js_urls(self) -> List[str]:
        return list([v for k, v in self._url_dic.items() if k.endswith('_js')])

    @property
    def css_urls(self) -> List[str]:
        return list([v for k, v in self._url_dic.items() if k.endswith('_css')])

    def set_file_url(self, url: str, name: str):
        self._url_dic[name] = url

    def set_cns(self, cns):
        self.cns.update(cns)

    def iter_local_paths(self):
        for name in self._url_dic.keys():
            url, local_path = self._localize_url(name)
            yield name, url, local_path

    def _localize_url(self, name: str, as_url=False):
        url = self._url_dic[name]
        if name == 'palette_css':
            local_path = '/'.join([self.name, self.theme_palette]) + '.min.css'
        else:
            filepath = url.rsplit('/')[-1]
            local_path = self.name + '/' + filepath
        if as_url:
            local_path = '/static/' + local_path
        return url, local_path

    def local_theme(self) -> 'Theme':
        new_theme = Theme(self.theme, self.theme_palette, is_local=True)
        new_theme.cns = self.cns
        for name, url in self._url_dic.items():
            new_theme.set_file_url(self._localize_url(url)[1], name)
        return new_theme

    def list_staticfiles(self):
        yield from self.css_urls
        yield from self.js_urls

    @classmethod
    def create_empty(cls, theme, theme_palette):
        return cls(theme, theme_palette)


def module2dict(module_path: str) -> dict:
    settings_module = importlib.import_module(module_path)
    settings_dict = {k: v for k, v in settings_module.__dict__.items() if k.isupper() and not k.startswith('_')}
    return settings_dict


class ThemeManager:
    def __init__(self, theme_app_config: dict = None, file2url: Dict = None):
        self.theme_app_config = theme_app_config or {}
        self.theme_name = theme_app_config.get('NAME')
        self.file2url = file2url or {}

        self._palette_css_fmt = self.theme_app_config.get('STATIC_URL_DICT', {}).get('palette_css')
        self._available_palettes = self.theme_app_config.get('PALETTES', [])

    def create_theme(self, theme_label: str, theme_app: str = None) -> Theme:
        if theme_app:
            settings_dict = module2dict(f'{theme_app}.config')
        else:
            settings_dict = self.theme_app_config
        theme_palette, theme_name, palette, is_local = parse_theme_label(theme_label)
        theme_obj = Theme.create_empty(theme_name, theme_palette)
        static_dic = settings_dict.get('STATIC_URL_DICT', {})
        palette_policy = settings_dict.get('PALETTE_POLICY')  # append / replace / none

        def _main_css(_url):
            if not (palette and palette_policy == 'replace'):
                theme_obj.set_file_url(_url, 'main_css')

        def _palette_css(_url):
            if palette:
                theme_obj.set_file_url(_url.format(palette=palette), 'palette_css')

        for f in _ORDERED_FIELDS_:
            val = static_dic.get(f)
            if not val:
                val = self.get_custom_url(theme_palette, f)
            if not val:
                continue
            if f == 'main_css':
                _main_css(val)
                continue
            if f == 'palette_css':
                _palette_css(val)
                continue
            if f.endswith('_js'):
                theme_obj.set_file_url(val, f)
            elif f.endswith('_css'):
                theme_obj.set_file_url(val, f)
            theme_obj.set_cns(settings_dict.get('CLASS_NAMES', {}))
        return theme_obj

    def get_custom_url(self, theme_label: str, name: str):
        return self.file2url.get(theme_label, {}).get(name, '')

    def table_css(self, border=False, borderless=False, striped=False, size=None) -> str:
        """Get class name for table element."""
        table_class_dic = self.theme_app_config.get('TABLE_CLASS_NAMES', '')
        cns = []

        def _get(_f, _v):
            if _v:
                _val = table_class_dic.get(_f, '')
                if _val:
                    cns.append(_val.format(**{_f: _v}))

        _get('default', 1)
        _get('border', border)
        _get('borderless', borderless)
        _get('borderless', borderless)
        _get('striped', striped)
        _get('size', size)
        return ' '.join(cns)

    @property
    def available_palettes(self) -> List[str]:
        return [self.theme_name] + [f'{self.theme_name}.{p}' for p in self._available_palettes]

    @classmethod
    def create_from_config_module(cls, theme_app: str, d2u: dict = None):
        theme_app_config = module2dict(f'{theme_app}.config')
        return cls(theme_app_config, d2u)
