import csv
import os
from urllib import parse

import click


@click.group(name='nipa')
def nipa_cli():
    pass


@nipa_cli.command('csvify')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
@click.option('-e', '--event', help='이벤트 이름(정상, 파손, 실신, 폭행, 돌진)')
def csvify(source_path, target_path, event):
    source_path = os.path.abspath(os.path.expanduser(source_path))
    target_path = os.path.abspath(os.path.expanduser(target_path))
    with open(source_path, 'r') as f:
        urls = f.read().split()
        with open(target_path, 'w', newline='') as f2:
            csv_writer = csv.writer(f2)
            csv_writer.writerow(
                ['meta_info.video.url', 'meta_info.extract_info.quality', 'meta_info.extract_info.resize_width',
                 'meta_info.extract_info.extract_per_seconds',
                 'meta_info.extract_info.extract_per_frames'])
            for url in urls:
                parsed_url = parse.urlparse(url)
                if event in parsed_url.path:
                    encoded_url = parse.quote(parsed_url.path)
                    result = 'https://nas-web-01.bluewhale.kr' + encoded_url
                    csv_writer.writerow([result, 100, 0, 0, None])



