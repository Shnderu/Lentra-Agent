import redis

class RedisQueue:
    def __init__(self, name: str):
        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )
        self.name = name

    def push(self, value: str):
        self.client.lpush(self.name, value)

    def pop(self):
        return self.client.rpop(self.name)


# TASKS
task_queue = RedisQueue("tasks")

def push_task(value: str):
    task_queue.push(value)

def pop_task():
    return task_queue.pop()


# RESULTS
result_queue = RedisQueue("results")

def push_result(value: str):
    result_queue.push(value)

def pop_result():
    return result_queue.pop()
