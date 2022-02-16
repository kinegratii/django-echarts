import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django_echarts.core.themes import get_theme
from django_echarts.utils.downloader import download_files
import prettytable


class Command(BaseCommand):
    help = 'Download the theme javascript and css files from remote.'

    def add_arguments(self, parser):
        parser.add_argument('theme', help='The name of a theme.')
        parser.add_argument(
            '--fake', '-f',
            action='store_true',
            help='Just print download meta info and do not download..'
        )
        parser.add_argument('--override', '-o', action='store_true')

    def handle(self, *args, **options):
        theme_name = options.get('theme')
        theme = get_theme(theme_name)
        file_info_list = []
        for url, local_path in theme.iter_local_paths():
            local_path = os.path.join(settings.BASE_DIR, 'static', local_path)
            file_info_list.append((url, local_path))
        if options.get('fake', False):
            table = prettytable.PrettyTable()
            table.field_names = ['RemoteUrl', 'LocalPath']
            table.add_rows(file_info_list)
            self.stdout.write(str(table))
        else:
            theme_dir = os.path.join(settings.BASE_DIR, 'static', theme.theme)
            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir)
            file_info_list = [info for info in file_info_list if not os.path.exists(info[1])]
            download_files(file_info_list)
            self.stdout.write(
                self.style.SUCCESS(f'Task Completed! You can use "{theme.name}#local" to the site config.'))
