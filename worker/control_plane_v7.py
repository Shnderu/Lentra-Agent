import redis
import json
import time
import uuid
import os
from collections import defaultdict

REDIS_HOST = os.getenv("REDIS_HOST", "lentra-redis")

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True
)

# ----------------------------
# CORE STREAMS
# ----------------------------
TASK_STREAM = "stream:rent:tasks"
RESULT_STREAM = "stream:rent:results"
DLQ_STREAM = "stream:rent:dlq"
REPLAY_STREAM = "stream:rent:replay"

# ----------------------------
# CONTROL PLANE STORAGE
# ----------------------------
WF_PREFIX = "wf:"
STATE_PREFIX = "task:state:"
TRACE_PREFIX = "trace:"
SLA_PREFIX = "sla:"

GROUP = "control-plane"
CONSUMER = f"cp-{os.getpid()}-{uuid.uuid4().hex[:6]}"

# ----------------------------
# IN-MEMORY METRICS (fast path)
# ----------------------------
metrics = defaultdict(int)


def now():
    return int(time.time())


# ----------------------------
# TRACING (distributed correlation)
# ----------------------------
def start_trace(task_id):
    trace_id = str(uuid.uuid4())
    r.hset(f"{TRACE_PREFIX}{task_id}", mapping={
        "trace_id": trace_id,
        "started_at": now()
    })
    return trace_id


def log_span(task_id, step, status, meta=None):
    r.rpush(f"{TRACE_PREFIX}{task_id}:spans", json.dumps({
        "step": step,
        "status": status,
        "ts": now(),
        "meta": meta or {}
    }))


# ----------------------------
# SLA TRACKING
# ----------------------------
def sla_start(task_id):
    r.hset(f"{SLA_PREFIX}{task_id}", mapping={
        "start": now(),
        "deadline": now() + 60
    })


def sla_check(task_id):
    data = r.hgetall(f"{SLA_PREFIX}{task_id}")
    if not data:
        return

    if now() > int(data.get("deadline", 0)):
        metrics["sla_breaches"] += 1
        set_state(task_id, "sla_breach")


# ----------------------------
# STATE
# ----------------------------
def set_state(task_id, status, extra=None):
    payload = {
        "status": status,
        "updated_at": now()
    }
    if extra:
        payload.update(extra)

    r.hset(f"{STATE_PREFIX}{task_id}", mapping=payload)


# ----------------------------
# WORKFLOW VERSIONING
# ----------------------------
def get_workflow(task_id):
    raw = r.get(f"{WF_PREFIX}{task_id}")
    if raw:
        return json.loads(raw)

    # default versioned workflow
    wf = {
        "version": "v1",
        "current": "step_0",
        "steps": [
            {"name": "step_0", "type": "rent.search"},
            {"name": "ai_enrich", "type": "enrich.ai"},
            {"name": "filter", "type": "filter.rules"}
        ]
    }
    r.set(f"{WF_PREFIX}{task_id}", json.dumps(wf))
    return wf


def save_workflow(task_id, wf):
    r.set(f"{WF_PREFIX}{task_id}", json.dumps(wf))


# ----------------------------
# REPLAY ENGINE
# ----------------------------
def enqueue_replay(task_id, step_name):
    r.xadd(REPLAY_STREAM, {
        "task_id": task_id,
        "step": step_name,
        "ts": now()
    })


def replay(task_id):
    wf = get_workflow(task_id)
    wf["current"] = "step_0"
    save_workflow(task_id, wf)

    r.xadd(TASK_STREAM, {
        "task_id": task_id,
        "type": "rent.search",
        "replay": 1
    })


# ----------------------------
# METRICS EMISSION
# ----------------------------
def emit_metrics():
    r.hset("metrics:queue", mapping={
        "tasks_processed": metrics["processed"],
        "errors": metrics["errors"],
        "sla_breaches": metrics["sla_breaches"],
        "ts": now()
    })


# ----------------------------
# CONTROL PLANE HANDLER
# ----------------------------
def handle_control_event(event):
    etype = event.get("type")

    if etype == "replay.task":
        replay(event["task_id"])

    if etype == "sla.check":
        sla_check(event["task_id"])

    if etype == "workflow.inspect":
        return get_workflow(event["task_id"])

    if etype == "trace.dump":
        return r.lrange(f"{TRACE_PREFIX}{event['task_id']}:spans", 0, -1)


# ----------------------------
# STREAM LOOP
# ----------------------------
def init_group():
    try:
        r.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
    except:
        pass


init_group()

print("LENTRA LEVEL 7 CONTROL PLANE ACTIVE (SAAS-GRADE ORCHESTRATION)")

last_metrics = 0

while True:
    try:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {TASK_STREAM: ">"},
            count=10,
            block=5000
        )

        if messages:
            for _, entries in messages:
                for msg_id, task in entries:

                    task_id = task.get("task_id")
                    metrics["processed"] += 1

                    sla_start(task_id)
                    start_trace(task_id)

                    log_span(task_id, "ingest", "ok")

                    set_state(task_id, "received")

                    emit_metrics()

                    r.xack(TASK_STREAM, GROUP, msg_id)

        # periodic metrics flush
        if time.time() - last_metrics > 10:
            emit_metrics()
            last_metrics = time.time()

    except Exception as e:
        metrics["errors"] += 1
        print("[CONTROL_PLANE_ERROR]", str(e))
        time.sleep(2)
