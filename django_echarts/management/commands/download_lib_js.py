# coding=utf8


from ._download import DownloadBaseCommand


class Command(DownloadBaseCommand):
    help = 'Download one or some library javascript files from remote CDN to project staticfile dirs.'

    def get_remote_url(self, pro_dj_settings, pro_echarts_settings, js_name, js_host):
        return pro_echarts_settings.resolve_url(
            dep_name=js_name,
            repo_name=js_host
        )
