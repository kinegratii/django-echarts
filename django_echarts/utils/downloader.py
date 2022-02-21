import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def download_file(remote_url: str, local_path: str):
    parent = os.path.dirname(local_path)
    if not os.path.exists(parent):
        os.mkdir(parent)
    filename = local_path.split('/')[-1]
    print(f'Download file {filename} start!')
    rsp = urllib.request.Request(
        remote_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
    )
    with urllib.request.urlopen(rsp) as response, open(local_path, 'w+b') as out_file:
        data = response.read()
        out_file.write(data)

    print(f'File {filename} download success!')


def download_files(file_info_list: list):
    with ThreadPoolExecutor() as executor:
        for remote_url, local_path in file_info_list:
            executor.submit(download_file, remote_url, local_path)
