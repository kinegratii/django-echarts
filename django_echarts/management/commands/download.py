# coding=utf8


import os
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS


class Command(BaseCommand):
    """
    A base command for download one or some js files. The subclasses can overwrite methods to specify its own remote url.
    """
    help = 'Download one or some javascript files from remote CDN to project staticfile dirs.'

    def add_arguments(self, parser):
        parser.add_argument('js_name', nargs='+', type=str)

        parser.add_argument(
            '--js_host',
            dest='js_host',
            help='The host where the file will be downloaded from.'
        )
        parser.add_argument(
            '--fake', '-f',
            action='store_true',
            help='Print the remote url and local path.'
        )

    def handle(self, *args, **options):
        js_names = options['js_name']
        js_host = options.get('js_host')
        fake = options.get('fake', False)
        # Start handle
        fake_result = []
        for i, js_name in enumerate(js_names):
            remote_url = self.get_remote_url(settings, DJANGO_ECHARTS_SETTINGS, js_name, js_host)
            local_dir = DJANGO_ECHARTS_SETTINGS.get_local_dir(js_name)
            print(local_dir)

            local_url = DJANGO_ECHARTS_SETTINGS.generate_local_url(js_name)  # TODO Fix
            print(local_url)
            local_path = settings.BASE_DIR + local_url.replace('/', os.sep)  # url => path
            if os.path.exists(local_path):
                flag = '✓'
            else:
                flag = '✗'
            fake_result.append((remote_url, local_path, local_url))
            if fake:
                self.stdout.write('[Info] Download Meta for [{}]'.format(js_name))
                self.stdout.write('        Remote Url: {}'.format(remote_url))
                self.stdout.write('        Static Url: {}'.format(local_url))
                self.stdout.write('     ({})Local Path: {}'.format(flag, local_path))
            else:
                self.download_js_file(remote_url, local_path)

    def download_js_file(self, remote_url, local_path, **kwargs):
        self.stdout.write('[Info] Download file from {0}'.format(remote_url))
        self.stdout.write('[Info] Save file to {0}'.format(local_path))
        rsp = urllib.request.Request(
            remote_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
            }
        )
        with urllib.request.urlopen(rsp) as response, open(local_path, 'w+b') as out_file:
            data = response.read()
            out_file.write(data)
            self.stdout.write('[Success] Save success!')

    # ##########################

    def get_remote_url(self, pro_dj_settings, pro_echarts_settings, js_name, js_host):
        return DJANGO_ECHARTS_SETTINGS.resolve_url(dep_name=js_name, repo_name=js_host)
