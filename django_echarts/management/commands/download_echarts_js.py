# coding=utf8

from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import six

from django_echarts.utils import DJANGO_ECHARTS_SETTINGS


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
        remote_host_store = DJANGO_ECHARTS_SETTINGS.host_store
        local_host_store = DJANGO_ECHARTS_SETTINGS.create_local_host()
        if local_host_store:
            for js_name in js_names:
                remote_url = remote_host_store.generate_js_link(js_name, js_host=options['js_host'])
                local_path = local_host_store.generate_js_link(js_name)
                local_path = local_path.replace('/', os.sep)
                local_path = settings.BASE_DIR + local_path
                self.download_js_file(remote_url, local_path)
        else:
            self.stderr.write('No local host is specified.')

    def download_js_file(self, remote_url, local_path, **kwargs):
        self.stdout.write('Download file from {0}'.format(remote_url))
        self.stdout.write('Save file to {0}'.format(local_path))
        rsp = six.moves.urllib.request.Request(
            remote_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
            }
        )
        with six.moves.urllib.request.urlopen(rsp) as response, open(local_path, 'w+b') as out_file:
            data = response.read()
            out_file.write(data)
