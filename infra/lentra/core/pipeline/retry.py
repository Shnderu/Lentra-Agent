import time
import random


class RetryPolicy:

    def __init__(self, retries: int = 3, base_delay: float = 0.5):
        self.retries = retries
        self.base_delay = base_delay

    def execute(self, fn, *args, **kwargs):

        last_error = None

        for attempt in range(self.retries):
            try:
                return fn(*args, **kwargs)

            except Exception as e:
                last_error = e

                delay = self.base_delay * (2 ** attempt)
                jitter = random.uniform(0, 0.3)

                time.sleep(delay + jitter)

        raise last_error
