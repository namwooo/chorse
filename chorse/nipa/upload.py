import csv
import os
from urllib import parse

import click

from chorse.config import Config
from chorse.ssh import ssh_execute, get_ssh, close_ssh


def remove_unmasking_video(resource_path):
    command = f'find {resource_path} -type f ! -iname \*_masking.mp4 -exec rm' + ' {} \;'

    ssh = get_ssh(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    result = ssh_execute(ssh, command)
    result = result.read().decode('UTF-8').strip('\n')
    close_ssh(ssh)

    return result


def get_abnormal_urls(resource_path, created_at=None):
    ROOT_URL = 'https://nas-web-01.bluewhale.kr/bimmo/nipa/abnormal/'
    command = f'find {resource_path} \( -iname "*_masking.mp4" -or -iname "*_masking.mov" \) -type f -newerBt {created_at} -exec ls' + ' {} \;'
    ssh = get_ssh(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    result = ssh_execute(ssh, command)
    result = result.read().decode('UTF-8').strip('\n')
    close_ssh(ssh)

    result = result.read().decode('UTF-8').strip('\n')

    urls = []
    if result:
        files = result.split('\n')
        urls = [file.replace('/volume1/storage/bimmo/nipa/abnormal/', ROOT_URL) for file in files]

    return urls


def get_face_urls(resource_path):
    ROOT_URL = 'https://nas-web-01.bluewhale.kr/bimmo/nipa/face/'
    command = f'find {resource_path} \( -iname "*.mp4" -or -iname "*.mov" \) -type f -exec ls' + ' {} \;'
    ssh = get_ssh(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    result = ssh_execute(ssh, command)
    result = result.read().decode('UTF-8').strip('\n')
    close_ssh(ssh)

    print(result)

    urls = []
    if result:
        files = result.split('\n')
        urls = [file.replace('/volume1/storage/bimmo/nipa/face/', ROOT_URL) for file in files]

    return urls


@click.command('abnormal-csvify')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
@click.option('-q', '--quality', default=100, help='화질 100 -> 원본 화질')
@click.option('-w', '--resize-width', default=0, help='너비 조정, 0 -> 원본 너비')
@click.option('-ps', '--per-seconds', help='1초당 추출 할 프레임수')
@click.option('-pf', '--per-frames', help='')
@click.option('-fc', '--frame-count', help='일정 간격으로 추출할 총 프레임수')
def bimmo_abnormal_csvify(resource_path, target_path, quality, resize_width, per_seconds=None, per_frames=None, frame_count=None):
    """
    python run.py nipa csvify -s /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/url.txt -t /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/normal.csv -ps 0
    """

    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # i.e. '/volume1/storage/bimmo/nipa/abnormal/test' NAS 서버 폴더 경로
    result = remove_unmasking_video(resource_path)
    urls = get_abnormal_urls(resource_path)
    with open(f'{target_path}/upload_urls.csv', 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ['meta_info.video.url',
             'meta_info.extract_info.quality',
             'meta_info.extract_info.resize_width',
             'meta_info.extract_info.extract_per_seconds',
             'meta_info.extract_info.extract_per_frames',
             'meta_info.extract_info.extract_count'])
        for url in urls:
            parsed_url = parse.urlparse(url)
            encoded_path = parse.quote(parsed_url.path)
            result = parsed_url.scheme + '://' + parsed_url.netloc + encoded_path
            csv_writer.writerow([result, quality, resize_width, per_seconds, per_frames, frame_count])


@click.command('face-csvify')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
@click.option('-q', '--quality', default=100, help='화질 100 -> 원본 화질')
@click.option('-w', '--resize-width', default=0, help='너비 조정, 0 -> 원본 너비')
@click.option('-ps', '--per-seconds', help='1초당 추출 할 프레임수')
@click.option('-pf', '--per-frames', help='')
@click.option('-fc', '--frame-count', help='일정 간격으로 추출할 총 프레임수')
def bimmo_face_csvify(resource_path, target_path, quality, resize_width, per_seconds=None, per_frames=None, frame_count=None):
    """
    python run.py nipa face-csvify -s /Users/lucakim/bluewhale/chorse/resource/nipa/face/0928 -t /Users/lucakim/bluewhale/chorse/resource/nipa/face/0928/upload-urls.csv -fc 510
    """

    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # i.e. '/volume1/storage/bimmo/nipa/face/test' NAS 서버 폴더 경로
    urls = get_face_urls(resource_path)
    with open(f'{target_path}/upload_urls.csv', 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ['meta_info.video.url',
             'meta_info.extract_info.quality',
             'meta_info.extract_info.resize_width',
             'meta_info.extract_info.extract_per_seconds',
             'meta_info.extract_info.extract_per_frames',
             'meta_info.extract_info.extract_count'])
        for url in urls:
            print(url)
            parsed_url = parse.urlparse(url)
            encoded_path = parse.quote(parsed_url.path)
            result = parsed_url.scheme + '://' + parsed_url.netloc + encoded_path
            csv_writer.writerow([result, quality, resize_width, per_seconds, per_frames, frame_count])
