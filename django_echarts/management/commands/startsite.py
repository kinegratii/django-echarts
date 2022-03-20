import os.path
from datetime import date

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_echarts import __version__


class Command(BaseCommand):
    help = 'Auto generate site_views.py file.'

    def add_arguments(self, parser):
        parser.add_argument('output', type=str, help='The output file.')
        def_year = date.today().year
        parser.add_argument('--site-title', '-t', type=str, help='The title of site.', default='Echarts Demo')
        parser.add_argument('--empty', '-e', action='store_true')
        parser.add_argument('--start-year', '-y', type=int, help='The start year.', default=def_year)
        parser.add_argument('--powered-by', '-p', type=str, help='The principal of copyright.',
                            default='Django-Echarts')
        parser.add_argument('--force', '-f', action='store_true')

    def handle(self, *args, **options):
        output = options.get('output')
        if output[-3:] != '.py':
            output += '.py'
        force = options.get('force', False)
        if not force and os.path.exists(output):
            self.stdout.write(self.style.ERROR(f'The file {output} exists! Add -f to overwrite it.'))
            return
        site_title = options.get('site_title')
        start_year = options.get('start_year')
        powered_by = options.get('powered_by')
        empty_chart = options.get('empty', False)
        self.generate_code_spinet(output, site_title, start_year, powered_by, empty_chart)

    def generate_code_spinet(self, output, site_title, start_year, powered_by, empty_chart):
        context = {
            'site_title': site_title,
            'start_year': start_year,
            'powered_by': powered_by,
            'use_chart': not empty_chart,
            'version': __version__,
        }
        s = render_to_string('snippets/first_views.py.tpl', context=context)
        with open(output, 'w') as f:
            f.write(s)
        self.stdout.write(self.style.SUCCESS(f'File {output} generated success!'))
