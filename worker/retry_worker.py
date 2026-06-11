import redis
import time

from core.queue.streams import STREAM_DLQ

r = redis.Redis(host="redis", port=6379, decode_responses=True)

while True:
    items = r.xread({STREAM_DLQ: "0"}, count=10, block=5000)

    if not items:
        continue

    time.sleep(5)
