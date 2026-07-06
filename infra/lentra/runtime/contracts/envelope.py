import time
import hashlib
import json


class ExecutionEnvelope:
    """
    DTO ONLY.
    No business logic.
    No execution logic.
    """

    def build(self, task: dict) -> dict:
        payload = task.get("payload", {})

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        raw = f"{task.get('task_id')}:{task.get('type')}:{json.dumps(payload, sort_keys=True)}"

        return {
            "task_id": task.get("task_id"),
            "type": task.get("type"),
            "payload": payload,
            "retry": int(task.get("retry", 0)),
            "idempotency_key": hashlib.sha256(raw.encode()).hexdigest(),
            "ts": time.time()
        }
