import os
import shutil
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import join

import click
from PIL import Image


@click.group(name='imaging')
def imaging_cli():
    pass


@imaging_cli.command('transpose')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def transpose_under_folder(resource_path, target_path):
    resource_path = os.path.abspath(os.path.expanduser(resource_path))

    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    pool = ThreadPoolExecutor(max_workers=10)

    for path, files in walk(resource_path):
        print('path:', path)
        for file in files:
            if '.jpg' not in file:
                continue
            from PIL import ImageFile
            ImageFile.LOAD_TRUNCATED_IMAGES = True

            pool.submit(transpose, path, file)
            # t = threading.Thread(target=transpose, args=(path, file))
            # t.start()
    pool.shutdown(wait=True)


def transpose(path, file):
    try:
        image = Image.open(join(path, file))
        image = image.transpose(method=Image.ROTATE_270)
        save_path = join(path, file)
        image.save(join(path, file))
        print('saved:', save_path)
    except Exception as e:
        print('error:', e)
        # with open('/Users/lucakim/error.txt', 'w') as f:
        #     f.write(e)
        pass


def walk(root_path):
    for path, dirs, files in os.walk(root_path):

        if files:
            yield path, files


@imaging_cli.command('process-folder')
@click.option('--root_dir')
def process_folder(root_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path, dirs, files in os.walk(root_dir_path):
        path_depth = len(path.split('/'))
        print(path, path_depth)

        if path_depth == 5:
            folder_name = path.split('/')[-1]
            folder_name = '_'.join(folder_name.split('_')[-3:])
            os.rename(path, path.replace(os.path.basename(path), folder_name))


@imaging_cli.command('map-image')
@click.option('--root_dir')
@click.option('--target_dir')
def map_image(root_dir: str, target_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    target_dir_path = os.path.abspath(os.path.expanduser(target_dir))

    count = 0
    for path_t, dirs_t, files_t in os.walk(target_dir_path):
        for path_r, dirs_r, files_r in os.walk(root_dir_path):
            if os.path.basename(path_t) == os.path.basename(path_r):
                count += 1
                for file in files_r:
                    print(f'{path_r}/{file}')
                    print(f'{path_t}/{file}')
                    if not os.path.exists(f'{path_t}/증명사진/'):
                        os.mkdir(f'{path_t}/증명사진/')
                    if not os.path.exists(f'{path_t}/증명사진/{file}'):
                        shutil.copy2(f'{path_r}/{file}', f'{path_t}/증명사진/{file}')

    print(count)


@imaging_cli.command('no-photo')
@click.option('--root_dir')
def no_photo(root_dir: str):
    root_dir_path = os.path.abspath(os.path.expanduser(root_dir))
    for path_r, dirs_r, files_r in os.walk(root_dir_path):
        path_depth = len(path_r.split('/'))
        if path_depth == 5:
            if not '증명사진' in os.listdir(path_r):
                print(path_r)
