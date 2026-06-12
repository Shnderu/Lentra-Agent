import redis
import time
import json

STREAM_RETRY = "stream:rent:retry"
STREAM_DLQ = "stream:rent:dlq"

MAX_RETRY = 5
BASE_DELAY = 2


class RetryHandler:
    def __init__(self, r):
        self.r = r

    def schedule_retry(self, task):
        retry = int(task.get("retry", 0)) + 1

        if retry > MAX_RETRY:
            self.r.xadd(STREAM_DLQ, {
                **task,
                "status": "dead",
                "reason": "max_retries_exceeded",
                "ts": time.time()
            })
            return

        delay = BASE_DELAY ** retry

        self.r.xadd(STREAM_RETRY, {
            **task,
            "retry": retry,
            "run_at": time.time() + delay,
            "status": "retry_scheduled"
        })
