import redis
import json
import time
from core.service import RentCoreService

r = redis.Redis(host="redis", port=6379, decode_responses=True)
service = RentCoreService()

STREAM = "stream:rent:tasks"
GROUP = "group:rent-workers"
CONSUMER = "worker-1"

# init consumer group
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except:
    pass

print("LENTRA WORKER STARTED (V6.2 STREAM MODE)")

def process(message_id, data):
    payload = json.loads(data["payload"])

    result = service.search(payload)

    # update task state
    r.set(
        f"task:{data['id']}",
        json.dumps({
            "status": "done",
            "result": result.dict(),
            "updated_at": time.time()
        })
    )

    return True

while True:
    resp = r.xreadgroup(
        GROUP,
        CONSUMER,
        {STREAM: ">"},
        count=10,
        block=5000
    )

    if not resp:
        continue

    for _, messages in resp:
        for msg_id, data in messages:

            try:
                process(msg_id, data)
                r.xack(STREAM, GROUP, msg_id)

            except Exception as e:
                # DLQ
                r.xadd("stream:rent:dlq", {
                    "error": str(e),
                    "payload": json.dumps(data)
                })
