import time
import threading


class RateLimiter:
    def __init__(self, rate_per_sec: float):
        self.capacity = rate_per_sec
        self.tokens = rate_per_sec
        self.rate = rate_per_sec
        self.last = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            delta = now - self.last
            self.last = now

            self.tokens = min(self.capacity, self.tokens + delta * self.rate)

            if self.tokens < 1:
                sleep_time = (1 - self.tokens) / self.rate
                time.sleep(sleep_time)
                self.tokens = 0
            else:
                self.tokens -= 1
