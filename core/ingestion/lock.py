import time


def acquire_lock(r, task_id: str, ttl: int = 90) -> bool:
    return r.set(f"lock:task:{task_id}", "1", nx=True, ex=ttl)


def refresh_lock(r, task_id: str, ttl: int = 90) -> None:
    r.expire(f"lock:task:{task_id}", ttl)


def release_lock(r, task_id: str) -> None:
    r.delete(f"lock:task:{task_id}")
