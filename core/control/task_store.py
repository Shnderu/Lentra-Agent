import redis
import time
import json


class TaskStore:
    def __init__(self, r: redis.Redis):
        self.r = r

    def create(self, task_id: str, payload: dict):
        self.r.set(f"task:{task_id}:state", "created")
        self.r.set(f"task:{task_id}:attempts", 0)
        self.r.set(f"task:{task_id}:payload", json.dumps(payload))

    def set_state(self, task_id: str, state: str):
        self.r.set(f"task:{task_id}:state", state)

    def inc_attempt(self, task_id: str) -> int:
        return self.r.incr(f"task:{task_id}:attempts")

    def get_state(self, task_id: str):
        return self.r.get(f"task:{task_id}:state")
