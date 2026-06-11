import json
import time
import redis

from core.queue.event_bus import EventBus
from core.queue.delayed_queue import DelayedQueue
from core.reliability.idempotency import IdempotencyStore
from core.observability.metrics import Metrics
from core.service import RentCoreService
from core.domain import RentQuery

r = redis.Redis(host="redis", port=6379, decode_responses=True)

bus = EventBus()
delayed = DelayedQueue()
idem = IdempotencyStore()
metrics = Metrics()
service = RentCoreService()

print("LENTRA WORKER STARTED (V6.6 PRODUCTION MODE)")

while True:

    delayed.tick()

    event = bus.consume(block=1000)

    if not event:
        continue

    msg_id, data = event

    start = time.time()

    try:
        task_id = data["task_id"]

        if idem.exists(task_id):
            bus.ack(msg_id)
            continue

        payload = json.loads(data["payload"])

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
            "meta": {"version": "v6.6"}
        }

        task["updated_at"] = time.time()

        r.set("task:" + task_id, json.dumps(task))

        metrics.incr("tasks_completed")

        bus.ack(msg_id)

        print("DONE:", task_id)

    except Exception as e:
        print("ERROR:", str(e))
        bus.retry(msg_id, data)

    finally:
        metrics.observe_latency("worker_task", start)
