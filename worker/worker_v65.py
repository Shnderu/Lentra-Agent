import json
import time
import redis

from core.queue.lease_queue import LeaseQueue
from core.queue.delayed_queue import DelayedQueue
from core.queue.event_bus import EventBus
from core.service import RentCoreService
from core.domain import RentQuery

r = redis.Redis(host="redis", port=6379, decode_responses=True)

lease = LeaseQueue()
delayed = DelayedQueue()
bus = EventBus()
service = RentCoreService()

print("LENTRA WORKER STARTED (V6.5 KAFKA-LITE MODE)")

while True:

    # 1. handle delayed jobs
    delayed.tick()

    # 2. consume stream (event-driven)
    event = bus.consume(block=1000)

    if event:
        msg_id, data = event

        try:
            payload = json.loads(data["payload"])
            task_id = data["task_id"]

            raw = r.get("task:" + task_id)
            if not raw:
                bus.ack(msg_id)
                continue

            task = json.loads(raw)

            query = RentQuery(
                city=payload["city"],
                budget=payload["budget"]
            )

            result = service.search(query)

            task["status"] = "done"
            task["result"] = {
                "listings": [l.__dict__ for l in result.listings],
                "sources_used": result.sources_used,
                "meta": {"version": "v6.5_event_stream"}
            }

            r.set("task:" + task_id, json.dumps(task))

            bus.ack(msg_id)

            print("DONE EVENT:", task_id)

        except Exception as e:
            print("ERROR EVENT:", str(e))
            bus.retry(msg_id, data)
            continue

    time.sleep(0.2)
