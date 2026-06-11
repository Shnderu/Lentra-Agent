import json

DLQ_KEY = "queue:rent:dlq"


def push(r, task: dict, reason: str) -> None:
    r.lpush(DLQ_KEY, json.dumps({
        "task": task,
        "reason": reason
    }))
