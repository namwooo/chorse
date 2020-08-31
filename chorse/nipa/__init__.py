import click

from chorse.nipa.download import download_video, remove_result
from chorse.nipa.export import download, face_upload_count
from chorse.nipa.trim import validate_frame_count, list_folder
from chorse.nipa.upload import bimmo_abnormal_csvify, bimmo_face_csvify


@click.group(name='nipa')
def nipa_cli():
    pass


nipa_cli.add_command(bimmo_abnormal_csvify)
nipa_cli.add_command(bimmo_face_csvify)
nipa_cli.add_command(download)
nipa_cli.add_command(face_upload_count)
nipa_cli.add_command(validate_frame_count)
nipa_cli.add_command(list_folder)
nipa_cli.add_command(download_video)
nipa_cli.add_command(remove_result)
