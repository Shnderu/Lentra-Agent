import time
import json
from core.queue.lease_queue import LeaseQueue
from core.service import RentCoreService
from core.domain import RentQuery

queue = LeaseQueue()
service = RentCoreService()

print("LENTRA WORKER STARTED (V6.4 LEASE MODE)")

while True:
    task_id = queue.pop_lease()

    if not task_id:
        queue.requeue_expired()
        time.sleep(1)
        continue

    try:
        raw = queue.r.get("task:" + task_id)
        if not raw:
            queue.ack(task_id)
            continue

        task = json.loads(raw)
        payload = task["payload"]

        query = RentQuery(
            city=payload["city"],
            budget=payload["budget"]
        )

        result = service.search(query)

        task["status"] = "done"
        task["result"] = {
            "listings": [l.__dict__ for l in result.listings],
            "sources_used": result.sources_used,
            "meta": {"version": "v6.4_lease"}
        }

        queue.r.set("task:" + task_id, json.dumps(task))

        queue.ack(task_id)

        print("DONE:", task_id, len(result.listings))

    except Exception as e:
        print("FAIL:", task_id, str(e))
        queue.nack(task_id)
