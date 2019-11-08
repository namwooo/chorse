import os
from os.path import join

import click
from PIL import Image


@click.group(name='imaging')
def imaging_cli():
    pass


@imaging_cli.command('rotate')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
@click.option('-a', '--angle', type=int, help='반시계 방향 회전 각도')
def rotate(resource_path, target_path, angle):
    resource_path = os.path.abspath(os.path.expanduser(resource_path))

    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    file_listing = os.listdir(resource_path)
    for file in file_listing:
        image = Image.open(join(resource_path, file))
        image = image.rotate(angle=angle)
        image.save(join(target_path, file))
