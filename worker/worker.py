import redis
import json
import time

from sources.registry import run_all_sources

r = redis.Redis(host="redis", port=6379, decode_responses=True)

print("Lentra Data Layer Worker started")


def process(task):
    t = task["type"]

    # ---------------------------
    # REAL RENT SEARCH PIPELINE
    # ---------------------------
    if t == "rent.search":

        query = task["payload"]

        raw_listings = run_all_sources(query)

        return {
            "message": "real ingestion completed",
            "sources_used": ["faswaz", "facebook"],
            "results": raw_listings
        }

    # ---------------------------
    # SCRAPE STEP (future expansion)
    # ---------------------------
    if t == "rent.scrape":
        return {
            "message": "scrape step placeholder"
        }

    return {
        "message": "unknown task type",
        "input": task["payload"]
    }


while True:
    item = r.brpop("queue:rent:tasks", timeout=5)

    if not item:
        continue

    task_id = item[1]

    raw = r.get(f"task:{task_id}")
    task = json.loads(raw)

    print(f"[PROCESS] {task_id} | {task['type']}")

    task["status"] = "processing"
    r.set(f"task:{task_id}", json.dumps(task))

    time.sleep(1)

    result = process(task)

    task["status"] = "done"
    task["result"] = result
    task["updated_at"] = time.time()

    r.set(f"task:{task_id}", json.dumps(task))

    print(f"[DONE] {task_id}")
