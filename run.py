# -*- coding: utf8 -*-

import click

from chorse.nipa import nipa_cli


@click.group(name='main')
def main_cli():
    pass


main_cli.add_command(nipa_cli)

if __name__ == "__main__":
    main_cli()
