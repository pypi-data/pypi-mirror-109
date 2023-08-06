import typing as tp
import pathlib
import yaml

try:
    YamlLoader = yaml.CSafeLoader
except AttributeError:  # System does not have libyaml
    YamlLoader = yaml.SafeLoader


def read_yml(filename: tp.Union[str, pathlib.Path]) -> dict:
    filename = pathlib.Path(filename)
    assert filename.exists(), f'file "{filename.absolute()}" not exists'

    with open(filename, 'r') as f:
        pipeline = yaml.load(f, Loader=YamlLoader)

    return pipeline
