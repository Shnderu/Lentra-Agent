import redis
from core.control.task_store import TaskStore
from core.control.policy_engine import PolicyEngine
from core.control.state_machine import TaskState

r = redis.Redis(host="redis", port=6379, decode_responses=True)

store = TaskStore(r)
policy = PolicyEngine()

STREAM = "stream:rent:tasks"
GROUP = "workers"


def process(task):
    return True


while True:
    resp = r.xreadgroup(GROUP, "worker-1", {STREAM: ">"}, count=10, block=5000)

    if not resp:
        continue

    for _, messages in resp:
        for msg_id, data in messages:

            task_id = data["task_id"]

            store.set_state(task_id, TaskState.PROCESSING.value)
            attempt = store.inc_attempt(task_id)

            try:
                process(data)

                store.set_state(task_id, TaskState.COMPLETED.value)
                r.xack(STREAM, GROUP, msg_id)

            except Exception:
                if policy.should_retry(attempt):
                    store.set_state(task_id, TaskState.RETRYING.value)
                else:
                    store.set_state(task_id, TaskState.DLQ.value)

                r.xack(STREAM, GROUP, msg_id)
