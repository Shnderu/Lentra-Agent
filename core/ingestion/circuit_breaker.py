import time


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = {}
        # state[source] = {"failures": int, "opened_at": float}

    def allow(self, source: str) -> bool:
        s = self.state.get(source)
        if not s:
            return True

        if s["failures"] < self.failure_threshold:
            return True

        if time.time() - s["opened_at"] > self.reset_timeout:
            self.state[source] = {"failures": 0, "opened_at": 0}
            return True

        return False

    def record_success(self, source: str):
        self.state[source] = {"failures": 0, "opened_at": 0}

    def record_failure(self, source: str):
        s = self.state.get(source, {"failures": 0, "opened_at": 0})
        failures = s["failures"] + 1
        self.state[source] = {
            "failures": failures,
            "opened_at": time.time() if failures >= self.failure_threshold else s.get("opened_at", time.time())
        }
