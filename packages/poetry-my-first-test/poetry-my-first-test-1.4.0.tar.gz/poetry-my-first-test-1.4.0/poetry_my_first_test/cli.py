import click

from poetry_my_first_test.views.main import health


@click.group()
def cli():
    print("START")


cli.add_command(health)
