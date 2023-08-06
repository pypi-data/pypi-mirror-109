import copy
import hashlib
import json


def get_pipeline_hash(pipeline: dict):
    pipeline_tasks = pipeline['tasks']
    json_dump = json.dumps(pipeline_tasks, sort_keys=True).encode('utf-8')
    return hashlib.md5(json_dump).hexdigest()[:32]
