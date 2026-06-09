import redis
import os
import time

r = redis.Redis(host="redis", port=6379, decode_responses=True)

LOCK_KEY = "flyrum:migration:lock"


def acquire_lock():
    ok = r.set(LOCK_KEY, "1", nx=True, ex=300)
    if not ok:
        raise RuntimeError("MIGRATION LOCKED (redis distributed lock)")


def release_lock():
    r.delete(LOCK_KEY)


def wait_for_lock_clear():
    while r.get(LOCK_KEY):
        time.sleep(1)
