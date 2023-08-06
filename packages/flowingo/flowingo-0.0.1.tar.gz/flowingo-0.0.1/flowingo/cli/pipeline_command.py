import pathlib

import click

from ..pipelines import read_yml, validate_pipeline


@click.group()
def pipeline():
    """pipeline executable function"""
    pass


@pipeline.command()
@click.argument('filename', type=click.Path(exists=True, file_okay=True, readable=True))
def validate(filename: str):
    """manager executable function"""
    path = pathlib.Path(filename)
    pipeline = read_yml(path.absolute())
    valid = validate_pipeline(pipeline, path)

    if not valid:
        print(f'pipeline {filename} is NOT valid!')
        exit(not valid)

    print(f'pipeline {filename} is valid!')
    exit(0)
