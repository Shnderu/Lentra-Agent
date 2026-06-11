from fastapi import FastAPI
from pydantic import BaseModel
import time
import redis

from core.reliability.backpressure import BackpressureController
from core.reliability.idempotency import IdempotencyGuard
from core.queue.streams import STREAM_TASKS

app = FastAPI()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

bp = BackpressureController(r)
idem = IdempotencyGuard(r)


class TaskIn(BaseModel):
    type: str
    payload: dict


@app.post("/task")
def create_task(task: TaskIn):
    task_id = str(time.time_ns())

    if not bp.allowed():
        return {"error": "backpressure_active"}

    if not idem.acquire(task_id):
        return {"error": "duplicate_task"}

    r.xadd(STREAM_TASKS, {
        "task_id": task_id,
        "type": task.type,
        "payload": str(task.payload),
        "retry": 0
    })

    return {"task_id": task_id}
