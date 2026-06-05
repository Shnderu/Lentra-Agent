import redis


class RedisQueue:
    def __init__(self):
        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )
        self.queue_name = "tasks"

    def push(self, task: str):
        self.client.lpush(self.queue_name, task)

    def pop(self):
        return self.client.rpop(self.queue_name)


queue = RedisQueue()


def pop_task():
    return queue.pop()
