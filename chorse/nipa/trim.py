import csv
import os
from pathlib import Path

import click


@click.command('validate-frame-count')
@click.option('--root_path')
@click.option('--frame_count', type=int)
def validate_frame_count(root_path: str, frame_count=1000):
    root_path = Path(root_path).expanduser().resolve()
    count = 0
    for path, dirs, files in os.walk(root_path):
        # jpg 파일만 필터링
        images = [file for file in files if '.jpg' in file]
        image_count = len(images)
        if image_count == frame_count:
            delta = frame_count - image_count
            print(path, delta)
            count += 1

    print(count)


@click.command('list')
@click.option('--root_dir')
@click.option('--result_dir')
def list_folder(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    base_names = []
    for path, dirs, files in os.walk(root_dir_path):
        base_name = os.path.basename(os.path.normpath(path))
        base_names.append(base_name)
    with open(f'{result_dir}/안면인식_제출_인원.csv', 'w', newline='', encoding='utf-8') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ['name_birth_gender'])
        for base_name in base_names:
            try:
                csv_writer.writerow([base_name])
            except Exception as e:
                print(e)
                pass

