# coding=utf8


from ._download import DownloadBaseCommand


class Command(DownloadBaseCommand):
    help = 'Download one or some map javascript files from remote CDN to project staticfile dirs.'

    def get_remote_url(self, pro_dj_settings, pro_echarts_settings, js_name, js_host):
        return pro_echarts_settings.generate_map_js_link(
            js_name=js_name,
            js_host=js_host
        )
