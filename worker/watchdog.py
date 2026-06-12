import time
import json
import redis

from core.reliability.dlq import DLQ_STREAM, TASK_TIMEOUT_SEC


STREAM = "stream:rent:tasks"


def get_redis():
    return redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def main():
    r = get_redis()

    print("WATCHDOG V7 STARTED")

    while True:
        keys = r.keys("task:*")

        now = time.time()

        for k in keys:
            raw = r.get(k)
            if not raw:
                continue

            task = json.loads(raw)

            if task.get("state") != "processing":
                continue

            created = task.get("created_at", now)

            if now - created > TASK_TIMEOUT_SEC:
                task["state"] = "retry"
                task["reason"] = "timeout"

                r.set(k, json.dumps(task))

                r.xadd(STREAM, {"data": json.dumps(task)})

                print("[WATCHDOG] requeued:", task["id"])

        time.sleep(5)


if __name__ == "__main__":
    main()
