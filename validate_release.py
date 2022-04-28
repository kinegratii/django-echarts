"""Validate whl file by comparing with source files."""
import os
import zipfile
import pathlib
import re


def get_version():
    here = pathlib.Path(__file__).parent
    txt = (here / 'django_echarts' / '__init__.py').read_text()
    __version__ = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    return __version__


def source_file_list():
    filenames = []
    for cur_dir, dirs, files in os.walk("django_echarts"):
        for file in files:
            fs = os.path.join(cur_dir, file)
            if fs.endswith('.pyc'):
                continue
            filenames.append(fs.replace('\\', '/'))
    return filenames


def zip_file_list():
    version = get_version()
    whl_file_path = pathlib.Path('dist') / f'django_echarts-{version}-py3-none-any.whl'

    with zipfile.ZipFile(whl_file_path) as archive:
        zip_filenames = [zinfo.filename for zinfo in archive.infolist()]
    return zip_filenames


def validate():
    s_list = source_file_list()
    z_list = zip_file_list()

    missing_files = list(set(s_list) - set(z_list))
    if len(missing_files) == 0:
        print('Validate success!')
    else:
        print('Error!The following files are missing:')
        for name in missing_files:
            print(f'\t{name}')


if __name__ == '__main__':
    validate()
