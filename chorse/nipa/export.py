import csv
import os
from os.path import join
from urllib import parse, request

import click

from chorse.config import Config
from chorse.ssh import ssh_execute, get_ssh, close_ssh


@click.command('download')
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


@click.command('face-upload-count')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def face_upload_count(resource_path, target_path):
    """NAS 서버에 수집된 안면인식 수량 폴더로 리스팅할 목적으로 작성"""
    # i.e. '/volume1/storage/bimmo/nipa/abnormal/test' NAS 서버 폴더 경로
    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    urls = get_face_resources(resource_path)
    print(urls)
    with open(f'{target_path}/folders.csv', 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ['folder'])
        for url in urls:
            csv_writer.writerow([url])


def get_face_resources(resource_path):
    ROOT_URL = 'https://nas-web-01.bluewhale.kr/bimmo/nipa/face/'
    command = f'find {resource_path} \( -name "*_2" -or -name "*_1" -or -name "*_1(*" -or -name "*_2(*" \) -type d;'
    ssh = get_ssh(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)
    result = ssh_execute(ssh, command)
    result = result.read().decode('UTF-8').strip('\n')
    close_ssh(ssh)

    urls = []
    if result:
        files = result.split('\n')
        urls = [file.replace('/volume1/storage/bimmo/nipa/face/', '').replace('(증필)', '').replace('(증명사진필요', '') for file in files]
    return urls
