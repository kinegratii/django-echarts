NAME = 'bootstrap3'

PALETTES = [
    "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "lumen", "paper",
    "readable", "sandstone", "simplex", "slate", "spacelab", "superhero", "united", "yeti",
]

STATIC_URL_DICT = {
    'main_css': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
    'palette_css': 'https://bootswatch.com/3/{palette}/bootstrap.min.css',
    'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
    'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
}
# replace or append palette css with main css
PALETTE_POLICY = 'replace'

CLASS_NAMES = {'row': 'row', 'col': 'col-sm-12 col-md-{n}'}

TABLE_CLASS_NAMES = {
    'default': 'table table-responsive',
    'border': 'table-bordered',
    'borderless': 'table-borderless',
    'striped': 'table-striped',
    'size': 'table-{size}'
}
