import click


@click.command()
@click.option("--count", default=1, type=int, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def health(count, name):
    for _ in range(count):
        click.echo(f"Hello, {name}!")
