import click

from chorse.nipa.export import download
from chorse.nipa.upload import bimmo_abnormal_csvify, bimmo_face_csvify, copy_file


@click.group(name='nipa')
def nipa_cli():
    pass


nipa_cli.add_command(bimmo_abnormal_csvify)
nipa_cli.add_command(bimmo_face_csvify)
nipa_cli.add_command(download)
nipa_cli.add_command(copy_file)
