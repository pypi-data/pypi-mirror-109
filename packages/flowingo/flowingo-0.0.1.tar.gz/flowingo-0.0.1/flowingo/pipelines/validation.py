import pathlib
import yamale


pipeline_schema_path = pathlib.Path(__file__).parent / 'pipeline_schema.yml'
assert pipeline_schema_path.exists(), 'pipeline_schema.yml have to exist'


def validate_pipeline(pipeline: dict, pipeline_path: pathlib.Path) -> bool:
    # validate with schema
    schema = yamale.make_schema(pipeline_schema_path.absolute())

    try:
        yamale.validate(schema, [(pipeline, pipeline_path)], strict=True, _raise_error=True)
    except yamale.YamaleError as e:
        print(e)
        return False

    # validate sub-pipelines exists
    # extract all sub-files
    # TODO: extract sub-pipelines
    # TODO: validate cyclic dependencies in imports

    return True
