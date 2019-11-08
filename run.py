# -*- coding: utf8 -*-

import click

from chorse.imaging import imaging_cli
from chorse.nas import nas_cli
from chorse.nipa import nipa_cli


@click.group(name='main')
def main_cli():
    pass


main_cli.add_command(nipa_cli)
main_cli.add_command(imaging_cli)
main_cli.add_command(nas_cli)

if __name__ == "__main__":
    main_cli()
