import redis
import os
import json
import time

r = redis.Redis(host="redis", port=6379, decode_responses=True)

STREAM = "flyrum:event:stream"
DLQ = "flyrum:event:dlq"


def emit(event_type, payload):
    r.xadd(STREAM, {
        "type": event_type,
        "data": json.dumps(payload),
        "ts": time.time()
    })


def consume(last_id="$", block=5000):
    return r.xread({STREAM: last_id}, block=block)


def send_to_dlq(event):
    r.xadd(DLQ, event)
