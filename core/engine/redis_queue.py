import redis
import json
import time

class RedisQueue:
    def __init__(self, name):
        self.client = redis.Redis(host="redis", port=6379, decode_responses=True)
        self.name = name

    def push(self, obj: dict):
        self.client.lpush(self.name, json.dumps(obj))

    def pop(self):
        raw = self.client.rpop(self.name)
        return json.loads(raw) if raw else None


task_queue = RedisQueue("tasks")
result_queue = RedisQueue("results")
failed_queue = RedisQueue("failed")


def push_task(task):
    task_queue.push(task)


def pop_task():
    return task_queue.pop()


def push_result(result):
    result_queue.push(result)


def push_failed(task):
    failed_queue.push(task)
