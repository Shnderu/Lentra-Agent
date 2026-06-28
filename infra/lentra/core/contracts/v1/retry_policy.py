import hashlib
import json


MAX_RETRIES = 3


def make_idempotency_key(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def should_retry(retry_count: int) -> bool:
    return retry_count < MAX_RETRIES


def next_retry_count(current: int) -> int:
    return current + 1
