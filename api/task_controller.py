import redis
from core.control.router import TaskRouter
from core.control.task_store import TaskStore
from core.control.state_machine import TaskState
from core.reliability.atomic_queue_v2 import AtomicQueueV2

r = redis.Redis(host="redis", port=6379, decode_responses=True)

router = TaskRouter()
store = TaskStore(r)
queue = AtomicQueueV2(r)


def create_task(task_id: str, task_type: str, payload: dict):
    stream = router.route(task_type)

    store.create(task_id, payload)
    store.set_state(task_id, TaskState.QUEUED.value)

    idem_key = f"idem:{task_id}"

    queue.push(stream, idem_key, task_id, payload)

    return {
        "task_id": task_id,
        "stream": stream,
        "state": "queued"
    }
