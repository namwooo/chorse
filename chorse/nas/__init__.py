import csv
import os
import threading
import urllib
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import join
from stat import S_ISDIR
from urllib import parse

import click

from chorse.config import Config
from chorse.ssh import get_sftp


@click.group(name='nas')
def nas_cli():
    pass


def sftp_walk(sftp, remote_path):
    path = remote_path
    folders = []
    files = []

    print(remote_path)
    file_listing = sftp.listdir_attr(path=remote_path)
    print(file_listing)
    for file in file_listing:
        if S_ISDIR(file.st_mode):
            folders.append(file.filename)
        else:
            files.append(file.filename)

    if files:
        yield path, files
    for folder in folders:
        new_path = os.path.join(remote_path, folder)
        for x in sftp_walk(sftp, new_path):
            yield x


@nas_cli.command('copy-file')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def copy_file(resource_path, target_path):
    ROOT_URL = 'https://nas-web-01.bluewhale.kr/bimmo/nipa/face/'
    """
    resource path i.e. /storage/bimmo/nipa/abnormal/0917/abnormal/0917
    target path i.e. ~/Desktop/test
    """
    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    sftp = get_sftp(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    # n = 0
    pool = ThreadPoolExecutor(max_workers=10)
    for path, files in sftp_walk(sftp, resource_path):
        for file in files:
            print('file:', file)
            print(path)
            url = path.replace('/storage/bimmo/nipa/face/', ROOT_URL) + '/' + file
            print(url)
            # print(path)
            # print(target_path +'/' + path)
            save_name = os.path.join(target_path + '/'+ path, file)
            # print(save_name)
            # print(url)
            if not os.path.exists(target_path +'/' + path):
                os.makedirs(target_path +'/' + path)
            # path = os.path.join(os.path.join(path, file))
            # n += 1
            # if any(x in path for x in ['A_정상', 'A_normal']):
            #     if not os.path.exists(target_path + '/normal'):
            #         os.makedirs(target_path + '/normal')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/normal', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['B_돌진', 'B_dash']):
            #     if not os.path.exists(target_path + '/dash'):
            #         os.makedirs(target_path + '/dash')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/dash', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['C_방치', 'C_abandon']):
            #     if not os.path.exists(target_path + '/abandon'):
            #         os.makedirs(target_path + '/abandon')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/abandon', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['D_2인', 'D_two_people']):
            #     if not os.path.exists(target_path + '/two_people'):
            #         os.makedirs(target_path + '/two_people')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/two_people', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['E_역방향', 'E_reverse']):
            #     if not os.path.exists(target_path + '/reverse'):
            #         os.makedirs(target_path + '/reverse')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/reverse', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['F_폭행', 'F_violence']):
            #     if not os.path.exists(target_path + '/violence'):
            #         os.makedirs(target_path + '/violence')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/violence', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['G_파손', 'G_damage']):
            #     if not os.path.exists(target_path + '/damage'):
            #         os.makedirs(target_path + '/damage')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/damage', str(n) + '.mp4'))
            #     continue
            # if any(x in path for x in ['H_실신', 'H_faint']):
            #     if not os.path.exists(target_path + '/faint'):
            #         os.makedirs(target_path + '/faint')
            #     sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + '/faint', str(n) + '.mp4'))
            #     continue
            # n += 1
            parsed_url = parse.urlparse(url)
            encoded_path = parse.quote(parsed_url.path)
            result = parsed_url.scheme + '://' + parsed_url.netloc + encoded_path
            print(result)
            pool.submit(download, result, save_name)
            # sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + path, file))
    sftp.close()
    pool.shutdown(wait=True)


def download(url, save_name):
    if not os.path.exists(save_name):
        urllib.request.urlretrieve(url, save_name)
