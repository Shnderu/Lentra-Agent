import time
import json
import uuid
import redis

class EventBus:
    """
    Kafka-like abstraction over Redis:
    - streams as event log
    - consumer groups
    - delayed jobs
    """

    def __init__(self, redis_host="redis", redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        self.stream = "stream:rent:tasks"
        self.dlq = "stream:rent:dlq"

        self.group = "workers"
        self.consumer = f"consumer-{uuid.uuid4().hex[:6]}"

        try:
            self.r.xgroup_create(self.stream, self.group, id="0", mkstream=True)
        except Exception:
            pass

    def publish(self, task_id: str, payload: dict):
        self.r.xadd(self.stream, {
            "task_id": task_id,
            "payload": json.dumps(payload),
            "ts": time.time()
        })

    def consume(self, block=5000):
        resp = self.r.xreadgroup(
            self.group,
            self.consumer,
            {self.stream: ">"},
            count=1,
            block=block
        )

        if not resp:
            return None

        stream, messages = resp[0]
        msg_id, data = messages[0]

        return msg_id, data

    def ack(self, msg_id):
        self.r.xack(self.stream, self.group, msg_id)

    def retry(self, msg_id, data):
        retries_key = f"retries:{data['task_id']}"
        retries = int(self.r.get(retries_key) or 0)

        if retries >= 5:
            self.r.xadd(self.dlq, data)
            self.r.xack(self.stream, self.group, msg_id)
            return

        self.r.incr(retries_key)
        time.sleep(min(2 ** retries, 30))

        self.r.xadd(self.stream, data)
        self.r.xack(self.stream, self.group, msg_id)
