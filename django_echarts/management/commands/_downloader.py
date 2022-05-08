import os
from typing import List

from django.core.management.base import BaseCommand

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS
from django_echarts.core.localfiles import DownloaderResource
from django_echarts.renders import get_js_dependencies
from django_echarts.stores.entity_factory import factory
from django_echarts.utils.downloader import download_files


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
        manager = DJANGO_ECHARTS_SETTINGS.dependency_manager
        return manager.get_download_resources(dep_names, repo_name)

    def resolve_theme(self, theme_name) -> List[DownloaderResource]:
        if theme_name:
            theme = DJANGO_ECHARTS_SETTINGS.create_theme(theme_name)
        else:
            theme = DJANGO_ECHARTS_SETTINGS.theme
        return DJANGO_ECHARTS_SETTINGS.theme_manger.get_download_resources(theme)

    def resolve_chart(self, chart_name) -> List[str]:
        chart_obj = factory.get_chart_widget(chart_name)
        if not chart_obj:
            self.stdout.write(self.style.WARNING('The chart with name does not exits.'))
            return []
        dep_names = get_js_dependencies(chart_obj)
        return dep_names
