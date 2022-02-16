import os.path
from datetime import date

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from django_echarts import __version__
from django_echarts.core.env_context import get_code_snippet_dir


class Command(BaseCommand):
    help = 'Auto generate site_views.py file.'

    def add_arguments(self, parser):
        parser.add_argument('output', type=str, help='The output file.')
        def_year = date.today().year
        parser.add_argument('--site-title', '-t', type=str, help='The title of site.', default='Echarts List')
        parser.add_argument('--start-year', '-y', type=int, help='The start year.', default=def_year)
        parser.add_argument('--powered-by', '-p', type=str, help='The principal of copyright.',
                            default='Django-Echarts')
        parser.add_argument('--override', '-o', action='store_true')

    def handle(self, *args, **options):
        output = options.get('output')
        if output[-3:] != '.py':
            output += '.py'
        override = options.get('override', False)
        if not override and os.path.exists(output):
            self.stdout.write(self.style.ERROR(f'The file {output} exists! Add -o to overwrite it.'))
            return
        site_title = options.get('site_title')
        start_year = options.get('start_year')
        powered_by = options.get('powered_by')
        self.generate_code_spinet(output, site_title, start_year, powered_by)

    def generate_code_spinet(self, output, site_title, start_year, powered_by):
        context = {
            'site_title': site_title,
            'start_year': start_year,
            'powered_by': powered_by,
            'version': __version__,
        }
        s = render_to_string(get_code_snippet_dir('first_views.py.tpl'), context=context)
        with open(output, 'w') as f:
            f.write(s)
        self.stdout.write(self.style.SUCCESS(f'File {output} generated success!'))
