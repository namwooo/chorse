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
@click.option('-ps', '--per-seconds', help='1초당 추출 할 프레임수')
@click.option('-fc', '--frame-count', help='일정 간격으로 추출할 총 프레임수')
def csvify(resource_path, target_path, per_seconds=None, frame_count=None):
    """
    python run.py nipa csvify -s /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/url.txt -t /Users/lucakim/bluewhale/chorse/resource/nipa/abnormal/0928/normal.csv -fc 500
    """
    source_path = os.path.abspath(os.path.expanduser(resource_path))
    target_path = os.path.abspath(os.path.expanduser(target_path))

    quality = 100
    resize_width = 0
    per_seconds = per_seconds
    per_frames = None
    frame_count = frame_count

    with open(source_path, 'r') as f:
        urls = f.read().split()
        with open(target_path, 'w', newline='') as f2:
            csv_writer = csv.writer(f2)
            csv_writer.writerow(
                ['meta_info.video.url', 'meta_info.extract_info.quality', 'meta_info.extract_info.resize_width',
                 'meta_info.extract_info.extract_per_seconds',
                 'meta_info.extract_info.extract_per_frames',
                 'meta_info.extract_info.extract_count'])
            for url in urls:
                parsed_url = parse.urlparse(url)
                encoded_path = parse.quote(parsed_url.path)
                result = parsed_url.scheme + '://' + parsed_url.netloc + encoded_path
                csv_writer.writerow([result, quality, resize_width, per_seconds, per_frames, frame_count])

