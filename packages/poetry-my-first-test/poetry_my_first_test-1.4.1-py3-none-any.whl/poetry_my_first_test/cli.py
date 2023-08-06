import click

from .views.main import health


@click.group()
def cli():
    print("START")


cli.add_command(health)
