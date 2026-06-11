import redis
from core.ingestion.processor import IngestionProcessorV5


r = redis.Redis(host="redis", port=6379, decode_responses=True)

processor = IngestionProcessorV5(r)

QUEUE = "queue:rent:tasks"

print("LENTRA WORKER STARTED (INGESTION V5)")


while True:
    item = r.brpop(QUEUE, timeout=5)
    if not item:
        continue

    _, task_id = item
    processor.run(task_id)
