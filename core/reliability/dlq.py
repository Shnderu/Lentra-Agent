import redis

STREAM_DLQ = "stream:rent:dlq"
STREAM_TASKS = "stream:rent:tasks"


class DLQProcessor:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def replay(self, group: str, consumer: str):
        items = self.r.xreadgroup(group, consumer, {STREAM_DLQ: ">"}, count=10)

        if not items:
            return

        for _, messages in items:
            for msg_id, data in messages:
                self.r.xadd(STREAM_TASKS, {
                    "task_id": data["task_id"],
                    "payload": data["payload"],
                    "retry": 0
                })

                self.r.xack(STREAM_DLQ, group, msg_id)
