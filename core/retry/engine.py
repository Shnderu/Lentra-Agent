import redis
import json
import time

r = redis.Redis(host="redis", port=6379, decode_responses=True)

DLQ = "flyrum:event:dlq"


def process_dlq():
    while True:
        items = r.xread({DLQ: "0-0"}, count=10, block=5000)

        if not items:
            continue

        for stream, messages in items:
            for msg_id, data in messages:
                print("[DLQ RETRY]", msg_id, data)
                # retry logic placeholder
                r.xdel(DLQ, msg_id)


if __name__ == "__main__":
    process_dlq()
