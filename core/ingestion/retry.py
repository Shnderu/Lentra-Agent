import time
import random


def compute_backoff(attempt: int) -> float:
    base = 1.5
    cap = 60
    jitter = random.uniform(0.0, 0.3)

    delay = min(cap, base ** attempt)
    return delay + jitter


def sleep_backoff(attempt: int) -> None:
    time.sleep(compute_backoff(attempt))
