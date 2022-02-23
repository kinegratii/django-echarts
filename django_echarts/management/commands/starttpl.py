import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand

from django_echarts.core.lib_context import get_django_echarts_template_dir


class Command(BaseCommand):
    help = 'Copy the builtin template files to your project templates.'

    def add_arguments(self, parser):
        """
        Examples:
            starttpl
            starttpl bootstrap5 # Print all template_names in this theme.
            starttpl bootstrap5 --all # Copy all template_names in this theme.
            starttpl -t bootstrap5 -n base # Copy templates/bootstrap5/base.html
        """
        parser.add_argument('theme', type=str, help='The name of theme.', default='bootstrap5',
                            choices=['bootstrap3', 'bootstrap5', 'material'])
        parser.add_argument('--tpl_name', '-n', nargs='+', type=str, help='The name list of template files.', )
        parser.add_argument('--all', '-a', action='store_true', help='Whether copy files for this theme.')
        parser.add_argument('--override', '-o', action='store_true', help='Whether to copy if the file exists.')

    def handle(self, *args, **options):
        theme_name = options.get('theme')
        template_names = options.get('tpl_name', [])
        copy_all = options.get('all', False)
        info_action = False
        if copy_all:
            template_names = self.get_all_template_names(theme_name)
        else:
            if not template_names:
                info_action = True
                template_names = self.get_all_template_names(theme_name)
        if info_action:
            self.stdout.write(f'The template names of Theme [{theme_name}]:')
            for name in template_names:
                self.stdout.write(f'\t{name}')
        else:
            override = options.get('override')
            self.copy_template_files(theme_name, template_names, override)

    def get_all_template_names(self, theme_name):
        theme_dir = get_django_echarts_template_dir(theme_name)
        template_names = [name for name in os.listdir(theme_dir)]
        return template_names

    def copy_template_files(self, theme_name, template_names, override):
        for no, template_name in enumerate(template_names, start=1):
            # TODO concat_str_if(template_name, '+.html')
            if template_name[-5:] != '.html':
                template_name += '.html'
            from_path = get_django_echarts_template_dir(theme_name, template_name)
            if not os.path.exists(from_path):
                self.stdout.write(self.style.WARNING(f'[Item #{no}] {template_name}, skipped!'))
            # TODO settings.TEMPLATES['DIR'][0]
            to_path = os.path.join(str(settings.BASE_DIR), 'templates', theme_name, template_name)
            if os.path.exists(to_path) and not override:
                self.stdout.write(self.style.WARNING(f'[Item #{no}] {template_name}, Exists!'))
            else:
                try:
                    os.makedirs(os.path.dirname(to_path), exist_ok=True)
                    shutil.copy(from_path, to_path)
                    self.stdout.write(self.style.SUCCESS(f'[Item #{no}] {template_name}, Success!'))
                except BaseException as e:
                    self.stdout.write(self.style.ERROR(f'[Item #{no}] {template_name}, Fail! {str(e)}'))
