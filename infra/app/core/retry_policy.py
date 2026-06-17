import time


class RetryPolicy:
    def __init__(self, max_retries=2, base_delay=0.05):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, fn, *args, **kwargs):
        last_err = None

        for i in range(self.max_retries + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_err = e
                time.sleep(self.base_delay * (i + 1))

        raise last_err
