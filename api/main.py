from fastapi import FastAPI
from pydantic import BaseModel
import time
import redis
import json

from core.queue.streams import STREAM_TASKS
from core.reliability.backpressure import BackpressureController

app = FastAPI()

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

bp = BackpressureController(r)


class TaskIn(BaseModel):
    type: str
    payload: dict


@app.post("/task")
def create_task(task: TaskIn):
    task_id = str(time.time_ns())

    # idempotency key
    idem_key = f"idem:{task_id}"
    if r.setnx(idem_key, 1) == 0:
        return {"error": "duplicate_task"}

    r.expire(idem_key, 3600)

    if not bp.allowed():
        return {"error": "backpressure_active"}

    r.xadd(STREAM_TASKS, {
        "task_id": task_id,
        "type": task.type,
        "payload": json.dumps(task.payload),
        "retry": 0,
        "status": "queued",
        "ts": time.time()
    })

    return {
        "task_id": task_id,
        "stream": STREAM_TASKS
    }
