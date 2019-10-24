import csv
import os
from os.path import join
from urllib import parse, request

import click
import paramiko

from chorse.nipa.ssh import get_ssh, close_ssh, ssh_execute


@click.group(name='nipa')
def nipa_cli():
    pass


# find file command
# find ./0929 -type f -iname \*_masking.mp4 -exec ls {} \;


HOST_IP = 'bluewhale.kr'
PORT = 40022
USERNAME = 'bluewhale'
PKEY = paramiko.RSAKey.from_private_key_file('/Users/lucakim/.ssh/jenkins_id_rsa')

ROOT_URL = 'https://nas-web-01.bluewhale.kr/bimmo/nipa/abnormal/'


def remove_file(resource_path):
    command = f'find {resource_path} -type f ! -iname \*_masking.mp4 -exec rm' + ' {} \;'

    ssh = get_ssh(HOST_IP, port=PORT, username=USERNAME, pkey=PKEY)
    result = ssh_execute(ssh, command)

    close_ssh(ssh)


def get_urls(resource_path):
    command = f'find {resource_path} -type f -iname \*_masking.mp4 -exec ls' + ' {} \;'
    ssh = get_ssh(HOST_IP, port=PORT, username=USERNAME, pkey=PKEY)
    result = ssh_execute(ssh, command)
    result = result.read().decode('UTF-8').strip('\n')

    urls = []
    if result:
        files = result.split('\n')
        urls = [file.replace('/volume1/storage/bimmo/nipa/abnormal/', ROOT_URL) for file in files]

    close_ssh(ssh)
    return urls


@nipa_cli.command('csvify')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
@click.option('-q', '--quality', default=100, help='화질 100 -> 원본 화질')
@click.option('-w', '--resize-width', default=0, help='너비 조정, 0 -> 원본 너비')
@click.option('-ps', '--per-seconds', default=0, help='1초당 추출 할 프레임수')
@click.option('-pf', '--per-frames', help='')
@click.option('-fc', '--frame-count', help='일정 간격으로 추출할 총 프레임수')
def bimmo_dataitem_upload_csvify(resource_path, target_path, quality, resize_width, per_seconds, per_frames=None, frame_count=None):
    """
    비모 데이터 아이템 업로드 및 프레임 추출 csv 파일 변환
    python run.py nipa csvify -s /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/url.txt -t /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/normal.csv -fc 500
    """

    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # i.e. '/volume1/storage/bimmo/nipa/abnormal/test' NAS 서버 폴더 경로
    urls = get_urls(resource_path)
    with open(f'{target_path}/test.csv', 'w', newline='') as f2:
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


@nipa_cli.command('download')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def download(resource_path, target_path):
    """
    개별 파일 다운로드
    python run.py nipa csvify -s /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/url.txt -t /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/normal.csv -fc 500
    """
    source_path = os.path.abspath(os.path.expanduser(resource_path))
    target_path = os.path.abspath(os.path.expanduser(target_path))

    with open(source_path, 'r') as f:
        urls = f.read().split('\n')
        for url in urls:

            parsed_url = parse.urlparse(url)
            child_dir = parsed_url.path.split('/')[5]
            target_dir = os.path.abspath(join(os.path.expanduser(target_path), child_dir))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            encoded_path = parse.quote(parsed_url.path)
            print(encoded_path)
            result = parsed_url.scheme + '://' + parsed_url.netloc + encoded_path

            request.urlretrieve(result, target_dir + '/' + parsed_url.path.split('/')[6])
