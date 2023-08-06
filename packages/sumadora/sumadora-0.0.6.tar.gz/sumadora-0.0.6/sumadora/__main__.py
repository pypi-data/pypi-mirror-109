import click

from sumadora.sumadora import sumar


@click.command()
@click.argument("numbers_string", nargs=-1, type=click.STRING)
def main(numbers_string):
    numbers_string = numbers_string.split()
    numbers_int = list(map(lambda num: int(num), numbers_string))
    result = sumar(numbers_int)
