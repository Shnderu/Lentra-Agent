import redis
import json
import time

from sources.registry import run_all_sources

from intelligence.normalizer import normalize_property
from intelligence.embedding import embed_item, embed_text
from intelligence.semantic_dedup import deduplicate
from intelligence.semantic_ranker import rank

r = redis.Redis(host="redis", port=6379, decode_responses=True)

print("Lentra Intelligence v2 Worker started")


def process(task):

    if task["type"] != "rent.search":
        return {"error": "unsupported"}

    query = task["payload"]
    query_text = query.get("city", "") + " rent apartment"

    # 1. ingestion
    raw = run_all_sources(query)

    # 2. normalization
    normalized = [normalize_property(x) for x in raw]

    # 3. embeddings
    item_embs = [embed_item(x) for x in normalized]
    query_emb = embed_text(query_text)

    # 4. semantic dedup
    unique_items, unique_embs = deduplicate(normalized, item_embs)

    # 5. re-embed after dedup alignment
    final_embs = [embed_item(x) for x in unique_items]

    # 6. ranking
    ranked = rank(unique_items, final_embs, query_emb)

    return {
        "message": "semantic intelligence v2 completed",
        "count": len(ranked),
        "results": ranked
    }


while True:
    item = r.brpop("queue:rent:tasks", timeout=5)

    if not item:
        continue

    task_id = item[1]

    raw = r.get(f"task:{task_id}")
    task = json.loads(raw)

    print(f"[INTEL-V2] {task_id}")

    task["status"] = "processing"
    r.set(f"task:{task_id}", json.dumps(task))

    time.sleep(1)

    result = process(task)

    task["status"] = "done"
    task["result"] = result
    task["updated_at"] = time.time()

    r.set(f"task:{task_id}", json.dumps(task))

    print(f"[DONE INTEL-V2] {task_id}")
