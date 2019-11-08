import os
from stat import S_ISDIR

import click

from chorse.config import Config
from chorse.ssh import get_sftp


@click.group(name='nas')
def nas_cli():
    pass


def sftp_walk(sftp, remote_path):
    path = remote_path
    folders = []
    files = []

    file_listing = sftp.listdir_attr(path=remote_path)
    for file in file_listing:
        if S_ISDIR(file.st_mode):
            folders.append(file.filename)
        else:
            files.append(file.filename)

    if files:
        yield path, files
    for folder in folders:
        new_path = os.path.join(remote_path, folder)
        for x in sftp_walk(sftp, new_path):
            yield x


@nas_cli.command('copy-file')
@click.option('-s', '--resource-path', help='소스 경로')
@click.option('-t', '--target-path', help='저장 경로')
def copy_file(resource_path, target_path):
    """
    resource path i.e. /storage/bimmo/nipa/abnormal/0917/abnormal/0917
    target path i.e. ~/Desktop/test
    """
    target_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    sftp = get_sftp(Config.HOST_IP, port=Config.PORT, username=Config.USERNAME, pkey=Config.PKEY)

    for path, files in sftp_walk(sftp, resource_path):
        for file in files:
            print(target_path + path)
            if not os.path.exists(target_path + path):
                os.makedirs(target_path + path)
            sftp.get(os.path.join(os.path.join(path, file)), os.path.join(target_path + path, file))

    sftp.close()
