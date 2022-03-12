import os
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.entities.chart_widgets import merge_js_dependencies
from django_echarts.starter.sites import DJESite
from django_echarts.utils.downloader import download_files


class DownloaderResource:
    def __init__(self, remote_url, ref_url, local_path, label=None, catalog=None, exists=False):
        self.remote_url = remote_url
        self.ref_url = ref_url
        self.local_path = local_path
        self.label = label or ''
        self.catalog = catalog or ''
        self.exists = exists


class DownloadBaseCommand(BaseCommand):

    def do_action(self, chart_names: List, dep_names: List, theme_name: str, repo_name: str, fake: bool):

        all_resources = []  # type: List[DownloaderResource]
        if theme_name:
            all_resources += self.resolve_theme(theme_name)
        all_dep_names = dep_names or []
        if chart_names:
            for cname in chart_names:
                all_dep_names += self.resolve_chart(cname)
        if all_dep_names:
            all_resources += self.resolve_dep(all_dep_names, repo_name)
        if fake:
            for i, res in enumerate(all_resources):
                if os.path.exists(res.local_path):
                    res.exists = True
                    msg = self.style.SUCCESS('        Local Path: {}'.format(res.local_path))
                else:
                    res.exists = False
                    msg = self.style.WARNING('        Local Path: {}'.format(res.local_path))
                self.stdout.write('[Resource #{:02d}] {}: Catalog: {}'.format(i + 1, res.label, res.catalog))
                self.stdout.write('        Remote Url: {}'.format(res.remote_url))
                self.stdout.write('        Static Url: {}'.format(res.ref_url))
                self.stdout.write(msg)
        else:
            file_info_list = [(res.remote_url, res.local_path) for res in all_resources if not res.exists]
            download_files(file_info_list)
            self.stdout.write(self.style.SUCCESS('Task completed!'))

    def resolve_dep(self, dep_names, repo_name) -> List[DownloaderResource]:
        resources = []
        manager = DJANGO_ECHARTS_SETTINGS.dependency_manager
        for dep_name, url, filename in manager.iter_download_resources(dep_names, repo_name):
            resources.append(DownloaderResource(
                url, '/static/' + filename, os.path.join(settings.BASE_DIR, 'static', filename),
                label=dep_name, catalog='Dependency'
            ))
        return resources

    def resolve_theme(self, theme_name) -> List[DownloaderResource]:
        if theme_name:
            theme = DJANGO_ECHARTS_SETTINGS.create_theme(theme_name)
        else:
            theme = DJANGO_ECHARTS_SETTINGS.theme
        resources = []
        for f_name, url, ref_url in theme.iter_local_paths():
            local_path = os.path.join(settings.BASE_DIR, 'static', ref_url)
            ref_url = '/static/' + ref_url
            resources.append(DownloaderResource(url, ref_url, local_path, label='', catalog=f_name))
        return resources

    def resolve_chart(self, chart_name) -> List[str]:
        site_obj = DJANGO_ECHARTS_SETTINGS.get_site_obj()  # type: DJESite
        chart_obj, func_exists, _ = site_obj.resolve_chart(chart_name)
        if not func_exists:
            self.stdout.write(self.style.WARNING('The chart with name does not exits.'))
            return []
        dep_names = merge_js_dependencies(chart_obj)
        return dep_names
