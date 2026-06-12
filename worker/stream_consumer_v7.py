import redis
import json
import time

STREAM = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = "worker-1"

r = redis.Redis(host="redis", decode_responses=True)

# ensure group exists
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except Exception:
    pass

print("STREAM CONSUMER STARTED V7")

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

    for stream, messages in resp:
        for msg_id, msg in messages:
            try:
                task = json.loads(msg.get("data", "{}"))

                print("[TASK]", task)

                # ACK after processing
                r.xack(STREAM, GROUP, msg_id)

            except Exception as e:
                print("[ERROR]", e)
