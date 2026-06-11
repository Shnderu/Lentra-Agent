import time
import json
import uuid
import redis
from typing import Optional

class LeaseQueue:
    """
    Redis-based lease queue:
    - push -> queue
    - pop -> lease (visibility timeout)
    - ack -> remove
    - nack -> retry or DLQ
    """

    def __init__(
        self,
        redis_host="redis",
        redis_port=6379,
        queue_name="queue:rent:tasks",
        retry_queue="queue:rent:retry",
        dlq="queue:rent:dlq",
        visibility_timeout=30,
        max_retries=3,
    ):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        self.queue = queue_name
        self.retry_queue = retry_queue
        self.dlq = dlq

        self.visibility_timeout = visibility_timeout
        self.max_retries = max_retries

        self.lease_prefix = "lease:"
        self.meta_prefix = "task:"

    def push(self, task_id: str):
        self.r.lpush(self.queue, task_id)

    def pop_lease(self) -> Optional[str]:
        task_id = self.r.rpop(self.queue)
        if not task_id:
            return None

        lease_id = str(uuid.uuid4())
        now = time.time()

        self.r.hset(self.lease_prefix + task_id, mapping={
            "lease_id": lease_id,
            "leased_at": now,
            "expires_at": now + self.visibility_timeout
        })

        return task_id

    def ack(self, task_id: str):
        self.r.delete(self.lease_prefix + task_id)

    def nack(self, task_id: str):
        lease_key = self.lease_prefix + task_id
        lease = self.r.hgetall(lease_key)

        retries_key = f"retries:{task_id}"
        retries = int(self.r.get(retries_key) or 0)

        if retries >= self.max_retries:
            self.r.lpush(self.dlq, task_id)
            self.r.delete(lease_key)
            return

        self.r.incr(retries_key)
        self.r.lpush(self.retry_queue, task_id)
        self.r.delete(lease_key)

    def requeue_expired(self):
        keys = self.r.keys(self.lease_prefix + "*")
        now = time.time()

        for k in keys:
            task_id = k.replace(self.lease_prefix, "")
            lease = self.r.hgetall(k)

            if not lease:
                continue

            if float(lease.get("expires_at", 0)) < now:
                self.r.lpush(self.queue, task_id)
                self.r.delete(k)
