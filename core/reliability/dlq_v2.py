import redis
import json

DLQ_STREAM = "stream:rent:dlq"


class DLQV2:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def push(self, task_id: str, payload: dict, error: str):
        self.r.xadd(DLQ_STREAM, {
            "task_id": task_id,
            "payload": json.dumps(payload),
            "error": error
        })

    def replay(self, target_stream: str, group: str, consumer: str):
        items = self.r.xreadgroup(group, consumer, {DLQ_STREAM: ">"}, count=10)

        if not items:
            return

        for _, messages in items:
            for msg_id, data in messages:
                self.r.xadd(target_stream, {
                    "task_id": data["task_id"],
                    "payload": data["payload"],
                    "retry": 0
                })

                self.r.xack(DLQ_STREAM, group, msg_id)
