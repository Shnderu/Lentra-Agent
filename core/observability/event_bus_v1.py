import time
import json
import redis
import uuid

"""
Lentra Observable Core v1
Event Bus Layer
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_EVENTS = "stream:observability:events"


class EventBus:

    def emit(self, event_type, payload):
        event = {
            "event_id": str(uuid.uuid4()),
            "type": event_type,
            "ts": time.time(),
            "payload": payload
        }

        r.xadd(STREAM_EVENTS, event)
        return event


bus = EventBus()


if __name__ == "__main__":
    print(bus.emit("test.event", {"hello": "world"}))
