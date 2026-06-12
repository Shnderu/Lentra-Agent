import redis
import os
import time

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True,
    socket_timeout=10,
    socket_connect_timeout=10,
    health_check_interval=30
)

GROUP = "workers"
CONSUMER = "worker-1"

STREAMS = [
    "stream:tasks:shard:0",
    "stream:tasks:shard:1"
]

VISIBILITY_ZSET = "queue:visibility"
DLQ = "stream:dlq"
RESULTS = "stream:results"

VISIBILITY_TIMEOUT = 30
MAX_RETRY = 5

for s in STREAMS:
    try:
        r.xgroup_create(s, GROUP, id="0", mkstream=True)
    except:
        pass


def lock_task(task_id, worker_id):
    now = time.time()
    return r.hset(f"task:{task_id}", mapping={
        "locked_by": worker_id,
        "locked_at": now,
        "status": "processing"
    })


def release_visibility():
    now = time.time()
    expired = r.zrangebyscore(VISIBILITY_ZSET, 0, now)

    for item in expired:
        task_id, stream, retry = item.split(":")

        r.zrem(VISIBILITY_ZSET, item)

        r.xadd(stream, {
            "task_id": task_id,
            "retry": int(retry) + 1,
            "status": "retry"
        })


def process(task):
    # BUSINESS LOGIC PLACEHOLDER
    if task.get("type") == "fail":
        raise Exception("forced failure")


while True:
    release_visibility()

    resp = r.xreadgroup(GROUP, CONSUMER, {
        STREAMS[0]: ">",
        STREAMS[1]: ">"
    }, count=10, block=5000)

    if not resp:
        continue

    for stream, entries in resp:
        for msg_id, data in entries:
            task_id = data["task_id"]
            retry = int(data.get("retry", 0))

            try:
                lock_task(task_id, CONSUMER)

                process(data)

                r.hset(f"task:{task_id}", "status", "done")

                r.xadd(RESULTS, data)

                r.xack(stream, GROUP, msg_id)

            except Exception as e:
                if retry >= MAX_RETRY:
                    r.hset(f"task:{task_id}", "status", "dead")
                    r.xadd(DLQ, data)
                else:
                    r.zadd(VISIBILITY_ZSET, {
                        f"{task_id}:{stream}:{retry}": time.time() + 10
                    })

                r.xack(stream, GROUP, msg_id)
