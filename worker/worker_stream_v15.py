import os
import json
import time
import redis

from core.queue.streams import STREAM_TASKS
from core.lifecycle.task_lifecycle import TaskLifecycleEngine, TaskContext, TaskStatus
from core.lifecycle.idempotency import IdempotencyGuard
from core.lifecycle.tracer import TaskTracer

from worker.handlers.rent_search import handle_rent_search


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

GROUP = "workers"
CONSUMER = "worker-1"

lifecycle = TaskLifecycleEngine()
idem = IdempotencyGuard(r)
tracer = TaskTracer(r)

try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except Exception:
    pass


def decode_task(data: dict) -> TaskContext:
    return TaskContext(
        task_id=data.get("task_id"),
        type=data.get("type"),
        payload=json.loads(data.get("payload", "{}")),
        retry=int(data.get("retry", 0)),
        status=TaskStatus(data.get("status", "queued")),
        ts=float(data.get("ts", time.time()))
    )


def route(task: TaskContext):
    if task.type == "rent.search":
        return handle_rent_search(task)
    return None


def process(task: TaskContext):

    tracer.start(task.task_id)

    if idem.is_processed(task.task_id):
        tracer.event(task.task_id, "duplicate_skip")
        return task

    idem.mark_processing(task.task_id)
    task = lifecycle.to_processing(task)

    tracer.processing(task.task_id)

    try:
        result = route(task)

        if result is None:
            raise Exception("No handler")

        task = lifecycle.to_done(task)
        idem.mark_done(task.task_id)

        tracer.success(task.task_id)

        r.xadd("stream:rent:results", {
            "task_id": task.task_id,
            "result": json.dumps(result),
            "status": task.status
        })

        return task

    except Exception as e:
        task = lifecycle.to_failed(task, str(e))
        idem.mark_failed(task.task_id)

        tracer.failed(task.task_id, str(e))

        if task.status == TaskStatus.RETRY:
            r.xadd("stream:rent:retry", {
                "task_id": task.task_id,
                "payload": json.dumps(task.payload),
                "retry": task.retry
            })
        else:
            r.xadd("stream:rent:dlq", {
                "task_id": task.task_id,
                "error": str(e),
                "payload": json.dumps(task.payload)
            })

        return task


print("STREAM WORKER V15 (OBSERVABLE EXECUTOR) ACTIVE")

while True:
    try:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_TASKS: ">"},
            count=10,
            block=5000
        )

        if not messages:
            continue

        for stream, entries in messages:
            for msg_id, data in entries:
                try:
                    task = decode_task(data)
                    process(task)
                    r.xack(STREAM_TASKS, GROUP, msg_id)
                    print("[OK]", task.task_id)

                except Exception as e:
                    print("[FATAL]", str(e))
                    r.xack(STREAM_TASKS, GROUP, msg_id)

    except Exception as e:
        print("[REDIS ERROR]", str(e))
        time.sleep(2)
