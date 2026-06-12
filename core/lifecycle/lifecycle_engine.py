import os
import redis
from core.queue.streams import STREAM_TASKS
from core.lifecycle.task_lifecycle import Task, TaskStatus


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)


class LifecycleEngine:

    def enqueue(self, task: Task):
        task.status = TaskStatus.QUEUED
        return r.xadd(STREAM_TASKS, task.to_stream())

    def mark_processing(self, task_id: str):
        # lightweight audit event
        return r.xadd(STREAM_TASKS, {
            "task_id": task_id,
            "status": TaskStatus.PROCESSING.value
        })

    def mark_done(self, task_id: str):
        return r.xadd(STREAM_TASKS, {
            "task_id": task_id,
            "status": TaskStatus.DONE.value
        })

    def mark_failed(self, task_id: str, reason: str = ""):
        return r.xadd(STREAM_TASKS, {
            "task_id": task_id,
            "status": TaskStatus.FAILED.value,
            "reason": reason
        })
