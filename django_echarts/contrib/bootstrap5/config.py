NAME = 'bootstrap5'

PALETTES = ["cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "litera", "lumen", "lux", "materia",
            "minty", "morph", "pulse", "quartz", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab",
            "superhero", "united", "vapor", "yeti", "zephyr",
            ]

STATIC_URL_DICT = {
    'main_css': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css',
    'palette_css': 'https://bootswatch.com/5/{palette}/bootstrap.min.css',
    'font_css': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css',
    'jquery_js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js',
    'main_js': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js',
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
