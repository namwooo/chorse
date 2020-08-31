# *- coding:utf-8 -*-
import os
import shutil
from pathlib import Path
from unicodedata import normalize

import click


@click.group(name='path')
def path_cli():
    pass


@path_cli.command('copy-file')
@click.option('-s', '--source-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def copy_file(source_path, target_path):
    source_path = Path(source_path).expanduser().resolve()
    target_path = Path(target_path).expanduser().resolve()

    for T_PATH in target_path.glob('*_*_*'):
        for S_PATH in source_path.glob('*_*_*'):
            if T_PATH.name == S_PATH.name:
                if not T_PATH.joinpath('bbox').exists():
                    T_PATH.joinpath('bbox').mkdir()

                for file in S_PATH.glob('*.json'):
                    # print(file)
                    print(T_PATH.joinpath('bbox').joinpath(file.name))
                    shutil.copy2(file, T_PATH.joinpath('bbox').joinpath(file.name))


def change_to_nfd_file(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        before = os.path.join(dirname, filename)
        after = normalize('NFD', before)
        os.rename(before, after)

        if os.path.isdir(before):
            change_to_nfd_file(before)
