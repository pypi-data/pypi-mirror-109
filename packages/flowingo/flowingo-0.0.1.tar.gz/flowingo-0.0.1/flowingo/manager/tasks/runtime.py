import datetime
import os
import time

from celery import Celery, Task, signature
from celery.canvas import chain, chord, Signature, group

from ..app import app, logger
from ...models import Pipeline, Session, Run


# TODO: type as TypedDict


class PipelineTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo) -> None:
        super(PipelineTask, self).on_failure(exc, task_id, args, kwargs, einfo)
        print(f'{task_id} failed: {exc}')

    def on_success(self, retval, task_id, args, kwargs) -> None:
        super(PipelineTask, self).on_success(retval, task_id, args, kwargs)
        print(f'{task_id} succeeded!')


@app.task(bind=True, name='flowingo._merge_context', shared=False)
def _merge_context(self: Task, contexts: list[dict]) -> dict:
    context = {}
    for i in contexts:
        context.update(i)
    return context


def _get_common_task(task_config: dict) -> Signature:
    task_name = task_config['task']
    parameters = task_config['parameters'] if 'parameters' in task_config else {}
    task_sign = signature(task_name, kwargs=parameters)

    return task_sign


def _get_task(task_config: dict) -> Signature:
    if 'group' in task_config:
        return _get_group_task(task_config['group'])

    if 'chain' in task_config:
        return _get_chain_task(task_config['chain'])

    if 'if' in task_config:
        return _get_if_task(task_config)

    return _get_common_task(task_config)


def _get_group_task(tasks_configs: list) -> Signature:
    tasks = []
    for task_config in tasks_configs:
        task_sign = _get_task(task_config)
        tasks.append(task_sign)

    _chord = chord(tasks, _merge_context.s())
    # _chord = group(tasks) | _merge_context.s()

    return _chord


def _get_chain_task(tasks_configs: list) -> Signature:
    if isinstance(tasks_configs, str):
        raise NotImplementedError
        # tasks_configs = _read_yml(tasks_configs)

    tasks = []
    for task_config in tasks_configs:
        task_sign = _get_task(task_config)
        tasks.append(task_sign)

    _chain = chain(*tasks)

    return _chain


@app.task(bind=True, name='flowingo._if', shared=False)
def _if_task(self: Task, context: dict, key=None, values=None) -> dict:
    if key not in context:
        return context

    value = context[key]

    if value in values:
        pipeline = signature('run_pipeline', kwargs=dict(filename=values[value]))
        return pipeline.delay(context).get(disable_sync_subtasks=False)

    if 'default' in values:
        pipeline = signature('run_pipeline', kwargs=dict(filename=values['default']))
        return pipeline.delay(context).get(disable_sync_subtasks=False)

    return context


def _get_if_task(tasks_config: dict) -> Signature:
    key = tasks_config['if']
    values = tasks_config['value']

    return _if_task.s(kwargs=dict(key=key, values=values))


@app.task(bind=True, name='flowingo._sub_pipeline', shared=False)
def _sub_pipeline(self: Task, context: dict, pipeline_id=None) -> dict:
    with Session.begin() as session:
        pipeline = session.get(Pipeline, pipeline_id)

        assert pipeline, 'pipeline_id must exist in database'

        tasks = pipeline.pipeline['tasks']

    _chain_task = _get_chain_task(tasks)
    _chain_task = _chain_task.replace(args=(context,))
    return self.replace(_chain_task)


@app.task(bind=True, name='flowingo._start_pipeline_run', shared=False)
def _start_pipeline_run(self: Task, context: dict, *args, pipeline_id=None, run_id=None):
    logger.info(f'Started pipeline {pipeline_id} with run {run_id}')
    logger.warn(f'context {context}, args {args}, pipeline_id= {pipeline_id}, run_id {run_id}')

    with Session.begin() as session:
        pipeline_run = session.get(Run, run_id)
        assert pipeline_run, 'run_id must exist in database'

        pipeline_run.start_timestamp = datetime.datetime.utcnow()

    return context


@app.task(bind=True, name='flowingo._end_pipeline_run', shared=False)
def _end_pipeline_run(self: Task, context: dict, pipeline_id=None, run_id=None):
    logger.info(f'Ending pipeline {pipeline_id} with run {run_id}')

    with Session.begin() as session:
        pipeline_run = session.get(Run, run_id)
        assert pipeline_run, 'run_id must exist in database'

        pipeline_run.end_timestamp = datetime.datetime.utcnow()

        # TODO: save output

    return context


@app.task(bind=True, name='flowingo.run_pipeline')
def run_pipeline(self: Task, context: dict, pipeline_id: int = None):
    logger.info(f'run_pipeline {pipeline_id}')
    assert pipeline_id, 'pipeline_id can not be None'

    context = context or {}
    # context['pipeline_id'] = pipeline_id

    with Session.begin() as session:
        pipeline = session.get(Pipeline, pipeline_id)

        assert pipeline, 'pipeline_id must exist in database'

        tasks = pipeline.pipeline['tasks']

        pipeline_run = Run(pipeline_id=pipeline.id, pipeline_dump_id=pipeline.dump_id)
        session.add(pipeline_run)
        session.flush()
        run_id = pipeline_run.id

    logger.info(f'run_pipeline tasks {tasks}')

    _chain_task = _get_chain_task(tasks)
    logger.info(f'run_pipeline tasks {_chain_task} args {_chain_task.args}')

    _run_pipeline_tasks = chain(
        _start_pipeline_run.s(pipeline_id=pipeline_id, run_id=run_id),
        _chain_task,
        _end_pipeline_run.s(pipeline_id=pipeline_id, run_id=run_id),
    )

    _run_pipeline_tasks = _run_pipeline_tasks.replace(args=(context,))
    logger.info(f'run_pipeline tasks {_run_pipeline_tasks} args {_run_pipeline_tasks.args}')

    return self.replace(_run_pipeline_tasks)
