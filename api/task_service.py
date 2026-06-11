import redis
from core.reliability.atomic_queue import AtomicQueue
from core.queue.streams import STREAM_TASKS

r = redis.Redis(host="redis", port=6379, decode_responses=True)

queue = AtomicQueue(r)


def create_task(task_id: str, payload: dict):
    idem_key = f"idem:task:{task_id}"

    ok = queue.push_task(
        STREAM_TASKS,
        idem_key,
        task_id,
        payload
    )

    if not ok:
        return {"status": "duplicate"}

    return {"status": "queued", "task_id": task_id}
