import redis
import json

r = redis.Redis(host="redis", decode_responses=True)

STREAM = "stream:rent:tasks"
GROUP = "workers"
CONSUMER = "worker-1"

try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except:
    pass

print("STREAM WORKER STARTED")

while True:
    messages = r.xreadgroup(
        GROUP,
        CONSUMER,
        {STREAM: ">"},
        count=10,
        block=5000
    )

    if not messages:
        continue

    for stream, entries in messages:
        for msg_id, data in entries:
            print("[TASK]", data)

            # TODO: business logic here

            r.xack(STREAM, GROUP, msg_id)
