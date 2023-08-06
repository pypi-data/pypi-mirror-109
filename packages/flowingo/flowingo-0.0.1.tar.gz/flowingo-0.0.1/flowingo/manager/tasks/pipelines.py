import pathlib
import typing as tp
import time
import os

import yaml
from sqlalchemy import select
from celery import Celery, Task, signature

from ..app import app, logger
from ...pipelines import read_yml, validate_pipeline, get_pipeline_hash
from ...models import Session, Pipeline, PipelineDump, PipelineTag


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls_collect_pipelines every 10 seconds.
    sender.add_periodic_task(10.0, _collect_pipelines.s(), name='collect pipelines every 10')


@app.task(bind=True, name='flowingo._refresh_pipeline', shared=False)
def _refresh_pipeline(self: Task, filepath: str) -> None:
    """Watch pipelines directory and list updated or new pipelines and it's status"""

    # read pipeline
    file = pathlib.Path(filepath)
    assert file.exists(), f'Pipeline file {filepath} must exists'
    filepath = str(file.absolute())
    pipeline_dict = read_yml(filepath)
    pipeline_hash = get_pipeline_hash(pipeline_dict)

    # validate pipeline
    pipeline_valid = validate_pipeline(pipeline_dict, file)

    if not pipeline_valid:
        logger.warn(f'pipeline {filepath} is not valid')
        assert pipeline_valid, 'pipeline must be valid'
        return

    # Cache file in dumps and update main pipeline object
    with Session.begin() as session:
        pipeline = session.execute(select(Pipeline).where(Pipeline.filepath == filepath)).scalar()

        if not pipeline:
            pipeline = Pipeline(pipeline=pipeline_dict, filepath=filepath)
            session.add(pipeline)
            session.flush()
            logger.info(f'Created pipeline {pipeline}')

        # update pipeline itself
        pipeline._update_from_dict(pipeline_dict)
        if 'tags' in pipeline_dict:
            tag_names = pipeline_dict['tags']

            existed_tag_names = [tag.name for tag in pipeline.tags]

            tags_to_delete = [tag for tag in pipeline.tags if tag.name not in tag_names]
            tags_names_to_create = [tag_name for tag_name in tag_names if tag_name not in existed_tag_names]

            for tag in tags_to_delete:
                session.delete(tag)
            session.add_all([PipelineTag(name=tag, pipeline_id=pipeline.id) for tag in tags_names_to_create])

            tags = session.execute(select(PipelineTag)).all()

        session.flush()

        # TODO: replace filenames with pipeline_dump id-s
        pipeline_dump = session.execute(select(PipelineDump).where(PipelineDump.pipeline_id == pipeline.id).where(PipelineDump.pipeline_hash == pipeline_hash)).scalar()

        # Exists exactly hashed pipeline.
        if pipeline_dump:
            # Ensure dump linked and exit
            pipeline.dump_id = pipeline_dump.id
            return

        # Update pipeline dump
        try:
            pipeline_dump = PipelineDump(pipeline_dict=pipeline_dict, pipeline=pipeline)
            session.add(pipeline_dump)
            pipeline.dump = pipeline_dump
            session.flush()
            logger.info(f'Created dump for pipeline {pipeline.id} with dump_id: {pipeline_dump.id}')
        except Exception as e:
            logger.warn(f'Exception: {e}')
            logger.warn(f'Could not create dump for pipeline {pipeline.id}')
            raise e


@app.task(bind=True, name='flowingo._collect_pipelines', shared=False)
def _collect_pipelines(self: Task) -> tp.List[tp.Tuple[str, str]]:
    """Watch pipelines directory and list updated or new pipelines and it's status"""

    logger.info('_collect_pipelines !!!!')

    # Compare existed caches. Update needed files

    return []

