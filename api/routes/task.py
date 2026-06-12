from core.queue.streams import STREAM_TASKS
import json
from fastapi import APIRouter

router = APIRouter()

@router.post("/task")
async def create_task(task: dict):
    import redis
    r = redis.Redis(host="redis", decode_responses=True)

    task_id = task.get("task_id", "auto")

    r.xadd(STREAM_TASKS, {
        "task_id": task_id,
        "data": json.dumps(task)
    })

    return {"task_id": task_id}
