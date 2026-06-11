import math


class PolicyEngine:
    def __init__(self):
        self.max_attempts = 5

    def should_retry(self, attempt: int) -> bool:
        return attempt < self.max_attempts

    def retry_delay(self, attempt: int) -> int:
        return min(2 ** attempt, 300)

    def priority_score(self, payload: dict) -> int:
        # future: budget, user tier, route importance
        return payload.get("priority", 1)
