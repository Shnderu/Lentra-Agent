import math


class RetryPolicy:
    def __init__(self, base_delay: int = 2, max_delay: int = 300):
        self.base = base_delay
        self.max = max_delay

    def get_delay(self, attempt: int) -> int:
        delay = self.base * math.pow(2, attempt)
        return int(min(delay, self.max))
