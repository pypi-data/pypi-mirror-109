import click

from sumadora.sumadora import sumar


@click.command()
@click.argument("numbers_string", type=click.STRING)
def cli(numbers_string):
    numbers_string = numbers_string.split()
    numbers_int = list(map(lambda num: int(num), numbers_string))
    result = sumar(*numbers_int)
    print(f"Result: {result}")


if __name__ == "__main__":
    cli()
