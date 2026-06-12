import time
import json
import redis

from core.reliability.dlq import DLQ_STREAM, TASK_TIMEOUT_SEC


def get_redis():
    return redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def main():
    r = get_redis()

    print("DLQ WORKER V7 STARTED")

    while True:
        items = r.xread({DLQ_STREAM: "0"}, count=10, block=5000)

        if not items:
            continue

        for _, messages in items:
            for msg_id, data in messages:
                task = json.loads(data["data"])
                print("[DLQ]", task)

        time.sleep(5)


if __name__ == "__main__":
    main()
