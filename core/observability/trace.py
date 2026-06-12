import uuid
import time


def new_trace_id():
    return str(uuid.uuid4())


def enrich(task: dict, trace_id: str = None):
    if not trace_id:
        trace_id = new_trace_id()

    task["trace_id"] = trace_id
    task["created_at"] = time.time()
    return task
