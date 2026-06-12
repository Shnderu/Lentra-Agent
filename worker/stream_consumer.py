import json
import os
import redis

from processor import process

STREAM_KEY = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = f"worker-{os.getenv('HOSTNAME', 'local')}"


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "lentra-redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True
    )


def ensure_group(r):
    try:
        r.xgroup_create(STREAM_KEY, GROUP, id="0", mkstream=True)
    except Exception:
        pass


def main():
    r = get_redis()
    ensure_group(r)

    print("V7 STREAM CONSUMER ACTIVE")

    while True:
        resp = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_KEY: ">"},
            count=10,
            block=5000
        )

        if not resp:
            continue

        for _, messages in resp:
            for msg_id, data in messages:
                try:
                    task = json.loads(data["data"])
                    process(task, r)
                    r.xack(STREAM_KEY, GROUP, msg_id)

                except Exception as e:
                    print("[STREAM ERROR]", e)
