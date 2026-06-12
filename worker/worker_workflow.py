import redis
import os
import time
import json

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

STREAM = "stream:wf:tasks"
RESULTS = "stream:wf:results"

GROUP = "wf-workers"
CONSUMER = "wf-1"

try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except:
    pass


def get_steps(wf_id):
    raw = r.get(f"wf:{wf_id}:steps")
    return json.loads(raw) if raw else {}


def check_ready(step_id, steps, done):
    deps = steps[step_id]["depends_on"]
    return all(d in done for d in deps)


def mark_done(wf_id, step_id, result):
    done_key = f"wf:{wf_id}:done"
    r.sadd(done_key, step_id)

    r.hset(f"wf:{wf_id}:result:{step_id}", mapping=result)


def schedule_next(wf_id, steps):
    done = r.smembers(f"wf:{wf_id}:done")

    for step_id, step in steps.items():
        if step_id in done:
            continue

        if check_ready(step_id, steps, done):
            r.xadd(STREAM, {
                "wf_id": wf_id,
                "step_id": step_id,
                "type": step["type"],
                "status": "queued"
            })


def process(step_type, payload):
    # MOCK AI / DOMAIN LOGIC
    return {
        "output": f"processed:{step_type}"
    }


while True:
    resp = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=5000)

    if not resp:
        continue

    for stream, entries in resp:
        for msg_id, data in entries:
            wf_id = data["wf_id"]
            step_id = data["step_id"]
            step_type = data["type"]

            steps = get_steps(wf_id)

            try:
                result = process(step_type, data)

                mark_done(wf_id, step_id, result)

                r.xadd(RESULTS, {
                    "wf_id": wf_id,
                    "step_id": step_id,
                    "result": str(result)
                })

                schedule_next(wf_id, steps)

                r.xack(STREAM, GROUP, msg_id)

            except Exception as e:
                r.xack(STREAM, GROUP, msg_id)
