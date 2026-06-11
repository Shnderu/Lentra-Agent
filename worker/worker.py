import json
import redis

from core.service import RentCoreService
from core.domain import RentQuery

r = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE = "queue:rent:tasks"
service = RentCoreService()

print("LENTRA WORKER STARTED (FIXED QUEUE MODE)")

while True:
    task = r.blpop(QUEUE, timeout=5)

    if not task:
        continue

    _, task_id = task

    raw = r.get(f"task:{task_id}")
    if not raw:
        continue

    job = json.loads(raw)

    payload = job["payload"]

    r.set(f"task:{task_id}", json.dumps({
        **job,
        "status": "running"
    }))

    query = RentQuery(
        city=payload.get("city"),
        budget=payload.get("budget"),
        min_price=payload.get("min_price"),
        max_price=payload.get("max_price"),
    )

    result = service.search(query)

    r.set(f"task:{task_id}", json.dumps({
        **job,
        "status": "done",
        "result": {
            "listings": [l.__dict__ for l in result.listings],
            "sources_used": result.sources_used,
            "meta": result.meta
        }
    }))

    print("processed:", task_id)
