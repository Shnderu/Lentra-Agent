import time


class RetryPolicy:
    """
    Simple exponential retry policy.
    """

    def should_retry(self, task: dict) -> bool:
        return int(task.get("retry", 0)) < 3

    def next_retry(self, task: dict) -> dict:
        task["retry"] = int(task.get("retry", 0)) + 1
        task["ts"] = time.time()
        return task
