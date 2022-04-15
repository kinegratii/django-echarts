from typing import Tuple
import os


class DownloaderResource:
    def __init__(self, remote_url, ref_url, local_path, label=None, catalog=None, exists=False):
        self.remote_url = remote_url
        self.ref_url = ref_url
        self.local_path = local_path
        self.label = label or ''
        self.catalog = catalog or ''
        self.exists = exists


class LocalFilesMixin:
    def set_localize_opts(self, static_url, staticfiles_dir):
        """Set options for localize_opts"""
        self._localize_opts = {
            'static_url': static_url,
            'staticfiles_dir': staticfiles_dir
        }

    def url2filename(self, url, **kwargs) -> str:
        pass

    def localize_url(self, filename: str) -> Tuple[str, str]:
        """Return local ref url and local file path from a remote url."""
        local_ref_url = self._localize_opts['static_url'] + filename
        local_path = os.path.join(self._localize_opts['staticfiles_dir'], filename)
        return local_ref_url, local_path
