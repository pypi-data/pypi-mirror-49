#!/usr/bin/env python3
"""
    mkalias.py - CLI app to create finder aliases.
"""
import os
import sys

import click

from .alias import Alias
from .log_helper import LogHelper
from .version import version


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('destination', type=click.Path(exists=True))
@click.option('--name', '-n', help='Set the name of the new alias')
@click.option('--debug', '-d', is_flag=True, help='Output all app info for testing/troubleshooting')
@click.version_option(version=version)
def main(source, destination, debug, name=None, ):
    log = LogHelper.init_logging(debug, __name__)

    log.debug('Source: "{}" \n'
              ' Destination: "{}"'.format(source, destination))

    source_path = os.path.abspath(source)
    destination_path = os.path.abspath(destination)

    log.info('Source Path: "{}" \n'
             ' Destination Path: "{}"'.format(source_path, destination_path))

    # Create the Alias
    alias_output = Alias.create(source_path, destination_path, name)

    log.info('Command String: "' + str(alias_output[Alias.CMD_STRING]) + '"')
    log.debug('osascript Exit Code: "' + str(alias_output[Alias.CODE]) + '"')
    log.debug('osascript Output: "' + str(alias_output[Alias.OUT]) + '"')
    log.debug('osascript Error: "' + str(alias_output[Alias.ERROR]) + '"')

    LogHelper.shutdown()
    sys.exit(0)  # exit gracefully


if __name__ == "__main__":
    main()
