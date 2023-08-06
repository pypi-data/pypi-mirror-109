import click
from actl import Application


@click.command()
@click.argument("application_directory")
@click.argument("command", default="")
def run(application_directory, command):
    app = Application(application_directory)
    app.run(command)
