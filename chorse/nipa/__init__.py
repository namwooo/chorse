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
def csvify(resource_path, target_path):
    source_path = os.path.abspath(os.path.expanduser(resource_path))
    target_path = os.path.abspath(os.path.expanduser(target_path))
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
                csv_writer.writerow([result, 100, 0, None, None, 500])



