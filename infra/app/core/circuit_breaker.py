import time


class CircuitBreaker:
    def __init__(self, fail_threshold=3, reset_timeout=5):
        self.fail_threshold = fail_threshold
        self.reset_timeout = reset_timeout

        self.fail_count = 0
        self.open_until = 0

    def allow(self):
        if time.time() < self.open_until:
            return False
        return True

    def success(self):
        self.fail_count = 0
        self.open_until = 0

    def fail(self):
        self.fail_count += 1

        if self.fail_count >= self.fail_threshold:
            self.open_until = time.time() + self.reset_timeout
            print("[CB] OPEN state activated")
