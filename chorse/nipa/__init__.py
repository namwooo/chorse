import click

from chorse.nipa import config
from chorse.nipa.config import Config
from chorse.nipa.export import download
from chorse.nipa.ssh import get_ssh, close_ssh, ssh_execute
from chorse.nipa.upload import bimmo_abnormal_csvify, bimmo_face_csvify


@click.group(name='nipa')
def nipa_cli():
    pass


nipa_cli.add_command(bimmo_abnormal_csvify)
nipa_cli.add_command(bimmo_face_csvify)
nipa_cli.add_command(download)
