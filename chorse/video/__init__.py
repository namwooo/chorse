import csv
import itertools
import os
import shutil
from pathlib import Path

import click


@click.group(name='video')
def video_cli():
    pass


@video_cli.command('transpose')
@click.option('--video_dir')
@click.option('--result_dir')
def transpose_video(video_dir: str, result_dir: str):
    video_dir_path = Path(video_dir).expanduser().resolve()
    for video_path in itertools.chain(video_dir_path.rglob('*.avi'), video_dir_path.rglob('*.MP4'), video_dir_path.rglob('*.mp4'),
                                      video_dir_path.rglob('*.MOV')):
        print(video_path, video_path.exists())

        path, filename = os.path.split(video_path)
        print(path)
        print(filename)
        frame_path = Path(f"{result_dir}/{path}")
        if not frame_path.exists():
            frame_path.mkdir(parents=True)

        if not os.path.exists(f"{str(frame_path)}/{filename}"):
            # os.system(f"ffmpeg -i \"{str(video_path)}\" -vf 'transpose=1' -b 10000k -preset ultrafast -threads 0 \"{str(frame_path)}/{filename}\"")
            os.system(
                f"ffmpeg -i \"{str(video_path)}\" -metadata:s:v:0 rotate=270 -c copy -b 10000k -preset ultrafast -threads 0 \"{str(frame_path)}/{filename}\"")


@video_cli.command('delete-video')
@click.option('--video_dir')
@click.option('--result_dir')
def delete_video(video_dir: str, result_dir: str):
    video_dir_path = Path(video_dir).expanduser().resolve()
    for video_path in itertools.chain(video_dir_path.rglob('*.avi'), video_dir_path.rglob('*.MP4'), video_dir_path.rglob('*.MOV')):
        print(video_path, video_path.exists())
        os.remove(video_path)


@video_cli.command('remove')
@click.option('--root_dir')
@click.option('--result_dir')
def remove(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        path_depth = len(path.split('/'))
        if path_depth == 8:
            print(path)
            try:
                os.rmdir(path)
                print(path)
            except Exception as e:
                print(e)
                pass


@video_cli.command('count')
@click.option('--root_dir')
@click.option('--result_dir')
def count(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        if len(files) > 1000:
            print(path)
            print(len(files) - 1000)


# @video_cli.command('count')
# @click.option('--root_dir')
# @click.option('--result_dir')
# def count(root_dir: str, result_dir: str):
#     root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
#     for path, dirs, files in os.walk(root_dir_path):
#         if len(files) > 1000:
#             for i in reversed(xrange(2)):
#                 # print(f'{path}/{i}')
#                 try:
#                     os.remove(f'{path}/{files[i]}')
#                 except FileNotFoundError as e:
#                     pass


@video_cli.command('exclude')
@click.option('--root_dir')
@click.option('--result_dir')
def count(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        for file in files:
            if len(file.split('.')[0]) == 3:
                os.remove(f'{path}/{file}')
                print(path)
                print(file)


@video_cli.command('list')
@click.option('--root_dir')
@click.option('--result_dir')
def count(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    base_names = []
    for path, dirs, files in os.walk(root_dir_path):
        base_name = os.path.basename(os.path.normpath(path))
        base_names.append(base_name)
    with open(f'{result_dir}/안면인식_제출_인원_원.csv', 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ['name_birth_gender'])
        for base_name in base_names:
            try:
                csv_writer.writerow([base_name])
            except Exception as e:
                print(e)
                pass


@video_cli.command('copy')
@click.option('--root_dir')
@click.option('--result_dir')
def count(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for i in range(0, 500):
        file_path = f'{root_dir_path}/1-{str(i).zfill(4)}.jpg'
        try:
            if not os.path.exists(file_path):
                print(f'{root_dir_path}/1-{str(int(i) - 1).zfill(4)}.jpg')
                shutil.copy(f'{root_dir_path}/1-{str(int(i) - 1).zfill(4)}.jpg', file_path)
        except Exception as e:
            print(e)

    for i in range(0, 500):
        file_path = f'{root_dir_path}/2-{str(i).zfill(4)}.jpg'
        try:
            if not os.path.exists(file_path):
                print(f'{root_dir_path}/1-{str(int(i) - 1).zfill(4)}.jpg')
                shutil.copy(f'{root_dir_path}/1-{str(int(i) - 1).zfill(4)}.jpg', file_path)
        except Exception as e:
            print(e)


@video_cli.command('delete')
@click.option('--root_dir')
@click.option('--result_dir')
def count(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        for file in files:
            if '2-' in file:
                if len(file) == 10:
                    os.remove(f'{path}/{file}')


@video_cli.command('merge')
@click.option('--root_dir')
@click.option('--result_dir')
def merge(root_dir: str, result_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        # print(path.split('/'))
        path_depth = len(path.split('/'))
        # print(path_depth)
        if path_depth < 7:
            continue
        for file in files:
            original_file_path = f'{path}/{file}'
            folder_number = original_file_path.split('/')[6]
            if folder_number == '1':
                prefix = '1-'
                file = prefix + file
            else:
                prefix = '2-'
                file = prefix + file

            save_path = '/'.join(original_file_path.split('/')[:6])

            try:
                # print(original_file_path)
                print(save_path)
                os.rename(original_file_path, f'{save_path}/{file}')
            except Exception as e:
                print(e)
                pass


@video_cli.command('compare')
@click.option('--root_dir')
def compare(root_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    original_list = []
    target_list = []

    with open(f'{root_dir_path}/안면인식_제출_인원_원.csv', 'r') as f:
        rdr = csv.reader(f)
        for line in rdr:
            original_list.append(line[0])

    with open(f'{root_dir_path}/안면인식_제출_인원.csv', 'r') as f2:
        rdr = csv.reader(f2)
        for line in rdr:
            target_list.append(line[0])
    a = set(original_list) - set(target_list)
    print(a)
