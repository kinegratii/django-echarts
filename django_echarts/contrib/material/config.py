NAME = 'material'

PALETTES = []

STATIC_URL_DICT = {
    'font_css': 'https://fonts.font.im/icon?family=Material+Icons',
    'main_css': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css',
    'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
    'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js',
}
# replace or append palette css with main css
PALETTE_POLICY = 'replace'

CLASS_NAMES = {'row': 'row', 'col': 'col s12 m{n}'}

TABLE_CLASS_NAMES = {
    'default': 'responsive-table',
    'striped': 'striped',
    'center': 'centered'
}
