from fastapi import FastAPI
from pydantic import BaseModel
import time
import redis
import hashlib

app = FastAPI()

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

SHARDS = 2
STREAM_PREFIX = "stream:tasks:shard:"
VISIBILITY_ZSET = "queue:visibility"
DLQ = "stream:dlq"

class TaskIn(BaseModel):
    type: str
    payload: dict

def shard(task_id: str):
    return int(hashlib.md5(task_id.encode()).hexdigest(), 16) % SHARDS

@app.post("/task")
def create_task(task: TaskIn):
    task_id = str(time.time_ns())
    shard_id = shard(task_id)

    stream = f"{STREAM_PREFIX}{shard_id}"

    r.set(f"idem:{task_id}", 1, nx=True, ex=3600)

    r.hset(f"task:{task_id}", mapping={
        "type": task.type,
        "payload": str(task.payload),
        "status": "queued",
        "retry": 0,
        "locked_by": "",
        "locked_at": 0
    })

    r.xadd(stream, {
        "task_id": task_id,
        "type": task.type,
        "payload": str(task.payload),
        "retry": 0,
        "status": "queued"
    })

    return {"task_id": task_id, "stream": stream}
