import os
import shutil

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import engines
from django_echarts.conf import DJANGO_ECHARTS_SETTINGS


def concat_if(s: str, fix: str):
    if s[-len(fix):] != fix:
        return s + fix
    else:
        return s


def get_theme_template_dir(app_name, *args) -> str:
    for app_config in apps.get_app_configs():
        if app_name in app_config.name:
            return os.path.join(app_config.path, 'templates', *args)


def get_dest_template_dir():
    django_engine = engines['django']
    if django_engine.dirs:
        return django_engine.dirs[0]
    else:
        return os.path.join(str(settings.BASE_DIR), 'templates')


class Command(BaseCommand):
    help = 'Copy the builtin template files to your project templates.'

    def add_arguments(self, parser):
        """
        Examples:
            starttpl
            starttpl bootstrap5 # Print all template_names in this theme.
            starttpl bootstrap5 --all # Copy all template_names in this theme.
            starttpl -t bootstrap5 -n base # Copy templates/base.html
            starttpl base
            starttpl blank -o my_page
            starttpl list all
        """
        parser.add_argument('--theme', type=str, help='The name of theme.', default='bootstrap5',
                            choices=['bootstrap3', 'bootstrap5', 'material'])
        parser.add_argument('tpl_name', type=str, nargs='+', help='The name of template file.', )
        parser.add_argument('--output', '-o', type=str, help='The output filename')
        parser.add_argument('--force', '-f', action='store_true', help='Whether to copy if the file exists.')

    def handle(self, *args, **options):
        theme_name = options.get('theme')
        if not theme_name:
            theme = DJANGO_ECHARTS_SETTINGS.theme
        else:
            theme = DJANGO_ECHARTS_SETTINGS.create_theme(theme_name)
        theme_name = theme.name
        template_names = options.get('tpl_name', [])
        if template_names:
            show_action = False
        else:
            template_names = self.get_all_template_names(theme_name)
            show_action = True
        if show_action:
            self.stdout.write(f'The template names of Theme [{theme_name}]:')
            for name in template_names:
                self.stdout.write(f'\t{name}')
            self.stdout.write('\n Start to custom a template: python manage.py starttpl -n blank -o my_page')
        else:
            template_name = template_names[0]
            output = options.get('output')
            force_action = options.get('force')
            self.copy_template_files(theme_name, template_name, output, force_action)

    def get_all_template_names(self, theme_name):
        theme_dir = get_theme_template_dir(theme_name)
        template_names = []
        for root, dirs, files in os.walk(theme_dir):
            for f in files:
                template_names.append(os.path.join(root, f)[len(theme_dir) + 1:])
        return template_names

    def copy_template_files(self, theme_name, template_name, output, force_action):
        template_name = concat_if(template_name, '.html')
        if output:
            output = concat_if(output, '.html')
        else:
            output = template_name
        from_path = get_theme_template_dir(theme_name, template_name)
        # From path
        if not os.path.exists(from_path):
            self.stdout.write(self.style.WARNING(f' {template_name}, skipped!'))
        pro_template_dir = get_dest_template_dir()
        to_path = os.path.join(pro_template_dir, output)
        if os.path.exists(to_path) and not force_action:
            self.stdout.write(self.style.WARNING(f' {output}, Exists! Add  -f option to override write.'))
        else:
            try:
                os.makedirs(os.path.dirname(to_path), exist_ok=True)
                shutil.copy(from_path, to_path)
                self.stdout.write(self.style.SUCCESS(f' {output}, Success!'))
            except BaseException as e:
                self.stdout.write(self.style.ERROR(f' {output}, Fail! {str(e)}'))
