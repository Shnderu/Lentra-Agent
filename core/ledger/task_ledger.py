import redis
import time
import json
from core.execution.state_machine import ExecutionStateMachine

class TaskLedger:
    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.key = "ledger:tasks"
        self.sm = ExecutionStateMachine()

    def register(self, task_id, payload):
        if self.r.hexists(self.key, task_id):
            return False

        self.r.hset(self.key, task_id, json.dumps({
            "status": "created",
            "payload": payload,
            "ts": time.time()
        }))
        return True

    def get(self, task_id):
        data = self.r.hget(self.key, task_id)
        return json.loads(data) if data else None

    def transition(self, task_id, event):
        state = self.get(task_id)
        if not state:
            return

        current = state["status"]
        next_state = self.sm.next(current, event)

        self.sm.validate(current, next_state)

        state["status"] = next_state
        state["ts"] = time.time()

        self.r.hset(self.key, task_id, json.dumps(state))
        return next_state
