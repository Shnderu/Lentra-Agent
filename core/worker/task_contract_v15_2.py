import json


ALLOWED_TASK_TYPES = {
    "send_message",
}


class TaskContractError(Exception):
    pass


def normalize_payload(payload):
    if payload is None:
        return {}

    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            raise TaskContractError("Invalid JSON payload")

    if isinstance(payload, dict):
        return payload

    raise TaskContractError("Unsupported payload type")


def validate_task(task_id, task_type, payload):
    if not task_id:
        raise TaskContractError("Missing task_id")

    if not task_type:
        raise TaskContractError("Missing task type")

    if task_type not in ALLOWED_TASK_TYPES:
        raise TaskContractError(f"Unknown task type: {task_type}")

    payload = normalize_payload(payload)

    return {
        "id": task_id,
        "type": task_type,
        "payload": payload
    }
