import click

# This controls entry on the usage line.
# @click.command(options_metavar='[[options]]')
@click.command()
@click.option('--count', default=1, help='number of greetings',
              metavar='<int>')
# @click.argument('name', metavar='<name>')
@click.argument('name')
def hello(name: str, count: int) -> None:
    """This script prints 'hello <name>' a total of <count> times."""
    click.echo(f"Hello from hello")
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()