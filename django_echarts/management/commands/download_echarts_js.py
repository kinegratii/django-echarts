# coding=utf8

from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import six

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS


class Command(BaseCommand):
    help = 'Download remote javascript to the local.'

    def add_arguments(self, parser):
        parser.add_argument('js_name', nargs='+', type=six.text_type)

        parser.add_argument(
            '--js_host',
            dest='js_host',
            help='The host where the file will be downloaded from.'
        )

    def handle(self, *args, **options):
        js_names = options['js_name']
        js_host = options.get('js_host')
        for js_name in js_names:
            remote_url = DJANGO_ECHARTS_SETTINGS.generate_js_link(js_name, js_host)
            local_url = DJANGO_ECHARTS_SETTINGS.generate_local_url(js_name)
            local_path = settings.BASE_DIR + local_url.replace('/', os.sep)  # url => path
            self.download_js_file(remote_url, local_path)

    def download_js_file(self, remote_url, local_path, **kwargs):
        self.stdout.write('[Info] Download file from {0}'.format(remote_url))
        self.stdout.write('[Info] Save file to {0}'.format(local_path))
        rsp = six.moves.urllib.request.Request(
            remote_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
            }
        )
        with six.moves.urllib.request.urlopen(rsp) as response, open(local_path, 'w+b') as out_file:
            data = response.read()
            out_file.write(data)
            self.stdout.write('[Success] Save success!')
