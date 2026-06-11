from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid
import time

r = redis.Redis(host="redis", port=6379, decode_responses=True)

app = FastAPI(title="Lentra Rent Core API")

class RentTask(BaseModel):
    type: str
    payload: dict

@app.post("/task")
def create_task(task: RentTask):

    task_id = str(uuid.uuid4())

    payload = {
        "id": task_id,
        "type": task.type,
        "payload": task.payload,
        "status": "queued",
        "result": None,
        "created_at": time.time(),
        "updated_at": time.time(),
        "meta": {
            "sources_enabled": ["faswaz", "facebook"]
        }
    }

    # V5 (legacy queue)
    r.set(f"task:{task_id}", json.dumps(payload))
    r.lpush("queue:rent:tasks", task_id)

    # V6 STREAM (event bus)
    r.xadd(
        "stream:rent:tasks",
        {
            "id": task_id,
            "type": task.type,
            "payload": json.dumps(task.payload)
        }
    )

    return {"task_id": task_id}

@app.get("/task/{task_id}")
def get_task(task_id: str):
    raw = r.get(f"task:{task_id}")
    if not raw:
        return {"error": "not found"}
    return json.loads(raw)
