import click
from . import singleton


def verbose(message: str, level=1):
    if singleton.verbosity >= level:
        click.echo(message)
