import redis
import json
import time
import os

STREAM = "stream:rent:tasks:shard:0"
GROUP = "workers"
CONSUMER = "worker-1"

REDIS_HOST = os.getenv("REDIS_HOST", "lentra-redis")

def create_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True,
        socket_timeout=10,
        socket_connect_timeout=10,
        retry_on_timeout=True,
        health_check_interval=30
    )

r = create_client()

def safe_call(fn, retries=5):
    global r
    last_err = None

    for i in range(retries):
        try:
            return fn(r)
        except Exception as e:
            last_err = e
            print("[REDIS RECOVER]", str(e))
            time.sleep(2 ** i)
            r = create_client()

    raise RuntimeError(f"Redis unavailable after retries: {last_err}")

try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except Exception:
    pass

print("STREAM WORKER V11 ACTIVE")

while True:
    try:
        messages = safe_call(lambda r: r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM: ">"},
            count=10,
            block=5000
        ))

        if not messages:
            continue

        for stream, entries in messages:
            for msg_id, data in entries:
                print("[TASK]", data)

                time.sleep(0.1)

                safe_call(lambda r: r.xack(STREAM, GROUP, msg_id))

    except Exception as e:
        print("[WORKER ERROR]", str(e))
        time.sleep(2)
