import redis
import json
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

STREAM_KEY = "lentra.events"


def publish(event_type: str, payload: dict):
    r.xadd(STREAM_KEY, {
        "type": event_type,
        "data": json.dumps(payload)
    })


def consume(last_id="0-0"):
    while True:
        events = r.xread({STREAM_KEY: last_id}, block=5000, count=10)
        if not events:
            continue

        for stream, messages in events:
            for msg_id, data in messages:
                yield msg_id, data
                last_id = msg_id
