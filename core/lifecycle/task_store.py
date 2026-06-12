import json
import time
import redis

from core.lifecycle.task_lifecycle import TaskStatus


class TaskStore:
    """
    Stores task state transitions in Redis (lightweight state DB layer).
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def create_task(self, task_id: str, task_type: str, payload: dict):
        self.r.hset(
            f"task:{task_id}",
            mapping={
                "task_id": task_id,
                "type": task_type,
                "payload": json.dumps(payload),
                "status": TaskStatus.CREATED.value,
                "retry": 0,
                "created_at": time.time()
            }
        )

    def update_status(self, task_id: str, status: TaskStatus):
        self.r.hset(
            f"task:{task_id}",
            "status",
            status.value
        )
        self.r.hset(
            f"task:{task_id}",
            "updated_at",
            time.time()
        )

    def get_task(self, task_id: str):
        return self.r.hgetall(f"task:{task_id}")
