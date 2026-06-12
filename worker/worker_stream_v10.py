import redis
import json
import time
import os
import uuid

REDIS_HOST = os.getenv("REDIS_HOST", "lentra-redis")

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True
)

TASK_STREAM = "stream:rent:tasks"
RESULT_STREAM = "stream:rent:results"
DLQ_STREAM = "stream:rent:dlq"
RETRY_ZSET = "stream:rent:retry:zset"

GROUP = "workers"
CONSUMER = f"worker-{os.getpid()}-{uuid.uuid4().hex[:6]}"

STATE_PREFIX = "task:state:"
WORKFLOW_PREFIX = "wf:"

MAX_RETRY = 3


def now():
    return int(time.time())


def state_key(task_id):
    return f"{STATE_PREFIX}{task_id}"


def set_state(task_id, status, extra=None):
    data = {
        "status": status,
        "updated_at": now()
    }
    if extra:
        data.update(extra)
    r.hset(state_key(task_id), mapping=data)


# ----------------------------
# WORKFLOW ENGINE (LEVEL 6)
# ----------------------------

def save_workflow(task_id, workflow):
    r.set(f"{WORKFLOW_PREFIX}{task_id}", json.dumps(workflow))


def get_workflow(task_id):
    raw = r.get(f"{WORKFLOW_PREFIX}{task_id}")
    return json.loads(raw) if raw else None


def next_step(workflow, current_step):
    steps = workflow.get("steps", [])
    for i, s in enumerate(steps):
        if s["name"] == current_step:
            if i + 1 < len(steps):
                return steps[i + 1]
    return None


def execute_step(step, payload):
    """
    Step execution engine
    """
    if step["type"] == "rent.search":
        city = payload.get("city", "unknown")

        time.sleep(0.2)

        return {
            "city": city,
            "hotels": 10,
            "avg_price": 1300,
            "currency": "USD"
        }

    if step["type"] == "enrich.ai":
        base = payload.get("result", {})
        base["ai_score"] = 0.87
        base["recommendation"] = "high-demand area"
        return base

    if step["type"] == "filter.rules":
        res = payload.get("result", {})
        res["filtered"] = True
        return res

    raise Exception(f"unknown step type: {step['type']}")


def push_result(task_id, result):
    r.xadd(RESULT_STREAM, {
        "task_id": task_id,
        "result": json.dumps(result),
        "ts": now()
    })


def push_dlq(task, error):
    r.xadd(DLQ_STREAM, {
        "task": json.dumps(task),
        "error": str(error),
        "ts": now()
    })


# ----------------------------
# WORKFLOW RUNNER
# ----------------------------

def run_workflow(task):
    task_id = task["task_id"]

    workflow = get_workflow(task_id)

    if not workflow:
        # default single-step workflow
        workflow = {
            "current": "step_0",
            "steps": [
                {"name": "step_0", "type": task["type"]},
                {"name": "ai_enrich", "type": "enrich.ai"},
                {"name": "rule_filter", "type": "filter.rules"}
            ]
        }
        save_workflow(task_id, workflow)

    current_name = workflow["current"]

    current_step = None
    for s in workflow["steps"]:
        if s["name"] == current_name:
            current_step = s
            break

    if not current_step:
        raise Exception("workflow corrupted")

    set_state(task_id, f"running:{current_name}")

    result = execute_step(current_step, task)

    workflow["last_result"] = result

    next_s = next_step(workflow, current_name)

    if next_s:
        workflow["current"] = next_s["name"]

        # pass result forward
        task["result"] = result

        save_workflow(task_id, workflow)

        # re-enqueue SAME task for next step
        r.xadd(TASK_STREAM, task)

    else:
        set_state(task_id, "done", {"result": json.dumps(result)})
        push_result(task_id, result)


# ----------------------------
# STREAM LOOP
# ----------------------------

def init_group():
    try:
        r.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
    except:
        pass


init_group()

print("LENTRA QUEUE LEVEL 6 ACTIVE (WORKFLOW ENGINE ENABLED)")

while True:
    try:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {TASK_STREAM: ">"},
            count=10,
            block=5000
        )

        if not messages:
            continue

        for _, entries in messages:
            for msg_id, task in entries:
                try:
                    run_workflow(task)
                    r.xack(TASK_STREAM, GROUP, msg_id)
                except Exception as e:
                    set_state(task.get("task_id"), "failed", {"error": str(e)})
                    push_dlq(task, str(e))
                    r.xack(TASK_STREAM, GROUP, msg_id)

    except Exception as e:
        print("[FATAL]", str(e))
        time.sleep(2)
