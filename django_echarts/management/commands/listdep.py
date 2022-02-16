import prettytable
from django.core.management.base import BaseCommand

from django_echarts.conf import DJANGO_ECHARTS_SETTINGS


class Command(BaseCommand):
    help = 'The manage command for dependency.'

    def add_arguments(self, parser):
        parser.add_argument('--dep_name', type=str, help='The name of dependency files.')

        parser.add_argument(
            '--repo_name',
            dest='repo_name',
            help='The name of a repository.'
        )
        parser.add_argument('--check_status', '-s', action='store_true', help='Check resource is access-ok.')

    def handle(self, *args, **options):
        dep_name = options.get('dep_name')
        repo_name = options.get('repo_name')
        check_status = options.get('check_status', False)
        if dep_name:
            self._show_dep_name(dep_name, check_status)
        else:
            if repo_name:
                pass
            else:
                self._list_all_repos()

    def _show_dep_name(self, dep_name, check_status=False):
        dm = DJANGO_ECHARTS_SETTINGS.dependency_manager
        table = prettytable.PrettyTable()
        if check_status:
            table.field_names = ['RepoName', 'DepUrl', 'Status']
        else:
            table.field_names = ['RepoName', 'DepUrl']
        catalog = ''
        for resource in dm.resolve_all_urls(dep_name):
            catalog = resource.catalog
            if check_status:
                table.add_row([resource.repo_name, resource.url, 'Success'])
            else:
                table.add_row([resource.repo_name, resource.url])
        self.stdout.write(f'DependencyName:{dep_name}')
        self.stdout.write(f'Catalog:{catalog}')
        table.add_autoindex('No.')
        self.stdout.write(str(table))

    def _list_all_repos(self):
        dm = DJANGO_ECHARTS_SETTINGS.dependency_manager
        table = prettytable.PrettyTable()
        table.field_names = ['Catalog', 'RepoName', 'RepoUrl']
        for c, n, u in dm.iter_repos():
            table.add_row([c, n, u])
        self.stdout.write(str(table))

    def _get_list(self, repo_name, dep_name):
        pass
