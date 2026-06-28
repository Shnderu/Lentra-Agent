import time
import random


class RetryExecutor:
    def __init__(self, retries: int = 3, base_delay: float = 0.3):
        self.retries = retries
        self.base_delay = base_delay

    def execute(self, fn):
        last_error = None

        for attempt in range(self.retries):
            try:
                return fn()
            except Exception as e:
                last_error = e

                # exponential backoff + jitter
                sleep_time = self.base_delay * (2 ** attempt)
                sleep_time += random.uniform(0, 0.1)

                time.sleep(sleep_time)

        raise last_error
