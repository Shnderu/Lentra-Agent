import redis
import time
import json
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

TIMERS = "zset:timers"
TASK_STREAM = "stream:wf:tasks"

while True:
    now = time.time()

    due = r.zrangebyscore(TIMERS, 0, now)

    for item in due:
        r.zrem(TIMERS, item)

        data = json.loads(item)

        r.xadd(TASK_STREAM, data)

    time.sleep(1)
