import json
import os
import shutil
import threading
import urllib
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from urllib import parse

import click

from chorse.config import Config
from chorse.ssh import get_sftp


@click.command('download-video')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def download_video(resource_path, target_path):
    target_path = Path(target_path).expanduser().resolve()
    resource_path = Path(resource_path).expanduser().resolve()

    if not target_path.exists():
        target_path.mkdir()

    with open(resource_path, 'r') as jf:
        json_data = json.load(jf)

        pool = ThreadPoolExecutor(max_workers=6)
        for data in json_data:
            dirname = data['dirname']
            url = data['url']
            target = ('/storage/bimmo/nipa/face/' + "/".join(url.split('/')[6:]))
            target = parse.unquote(target)
            prefix = data['file_prefix']
            frame_count = data['frame_count']
            extension = url.split('.')[-1]
            save_name = target_path / f'{dirname}-{prefix}-{frame_count}.{extension}'
            pool.submit(download, target, save_name)

        pool.shutdown(wait=True)


def download(target, save_name):
    sftp = get_sftp(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    print(save_name)
    try:
        if not save_name.exists():
            sftp.get(os.path.join(target), save_name)
    except:
        print('error', target)
        print('error', save_name)
        pass


@click.command('remove-result')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def remove_result(resource_path, target_path):
    target_path = os.path.abspath(os.path.expanduser(target_path))
    source_path = os.path.abspath(os.path.expanduser(resource_path))
    count = 0

    # for dirpath_t, dirnames_t, filenames_t in os.walk(target_path):
    #     for filename_t in filenames_t:
    #         temp_list = filename_t.split('.')[0].split('_')
    #         a = temp_list[0:2]
    #         b = temp_list[-1].split('-')[0]
    #         a.append(b)
    #         person = '_'.join(a)
    #         # print(person)
    #         for dirpath_s, dirnames_s, filenames_s in os.walk(source_path):
    #             for dirname_s in dirnames_s:
    #                 if person == dirname_s:
    #                     count +=1
    #                     print(source_path + '/' + person)
    #                     # shutil.rmtree(source_path +'/'+person)

    for dirpath_s, dirnames_s, filenames_s in os.walk(source_path):
            for dirpath_t, dirnames_t, filenames_t in os.walk(target_path):
                for filename_t in filenames_t:
                    person = filename_t.split('.')[0]
                    if person in dirnames_s:
                        os.remove(dirpath_t + '/' + filename_t)
                        count += 1

    print(count)
