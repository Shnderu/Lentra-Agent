import redis
import json
import time
import os
import uuid
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

TASK_STREAM = "stream:rent:tasks"
RESULT_STREAM = "stream:rent:results"
DLQ_STREAM = "stream:rent:dlq"
RETRY_ZSET = "stream:rent:retry:zset"

GROUP = "workers"
CONSUMER = f"worker-{os.getpid()}-{uuid.uuid4().hex[:6]}"

STATE_PREFIX = "task:state:"
LOCK_PREFIX = "task:lock:"
LEASE_PREFIX = "task:lease:"

MAX_RETRY = 3
LEASE_TTL = 30

inflight = defaultdict(float)


def now():
    return int(time.time())


def state_key(task_id):
    return f"{STATE_PREFIX}{task_id}"


def lock_key(task_id):
    return f"{LOCK_PREFIX}{task_id}"


def lease_key(task_id):
    return f"{LEASE_PREFIX}{task_id}"


def set_state(task_id, status, extra=None):
    data = {
        "status": status,
        "updated_at": now(),
        "worker": CONSUMER
    }
    if extra:
        data.update(extra)
    r.hset(state_key(task_id), mapping=data)


def acquire_lock(task_id):
    return r.set(lock_key(task_id), CONSUMER, nx=True, ex=60)


def renew_lease(task_id):
    r.set(lease_key(task_id), CONSUMER, ex=LEASE_TTL)


def check_single_flight(task_id):
    return inflight.get(task_id, 0) == 0


def mark_inflight(task_id):
    inflight[task_id] = time.time()


def clear_inflight(task_id):
    inflight.pop(task_id, None)


def get_retry(task):
    try:
        return int(task.get("retry", 0))
    except:
        return 0


def handle(task):
    task_type = task.get("type")
    payload = task.get("payload", {})

    if task_type == "rent.search":
        city = payload.get("city", "unknown")
        time.sleep(0.2)

        return {
            "city": city,
            "hotels": 7,
            "avg_price": 1200,
            "currency": "USD"
        }

    raise Exception(f"no handler: {task_type}")


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


def schedule_retry(task):
    retry = get_retry(task)

    if retry >= MAX_RETRY:
        push_dlq(task, "max_retry_reached")
        set_state(task.get("task_id"), "failed")
        return

    delay = min(2 ** retry, 60)
    run_at = now() + delay

    task["retry"] = retry + 1

    r.zadd(RETRY_ZSET, {
        json.dumps(task): run_at
    })

    set_state(task.get("task_id"), "retry_scheduled", {"run_at": run_at})


def process(task):
    task_id = task.get("task_id")

    if not check_single_flight(task_id):
        return

    mark_inflight(task_id)
    renew_lease(task_id)

    set_state(task_id, "processing")

    if not acquire_lock(task_id):
        clear_inflight(task_id)
        return

    try:
        result = handle(task)

        push_result(task_id, result)

        set_state(task_id, "done", {"result": json.dumps(result)})

    except Exception as e:
        set_state(task_id, "failed", {"error": str(e)})
        schedule_retry(task)

    finally:
        clear_inflight(task_id)
        r.delete(lease_key(task_id))


def drain_retry():
    items = r.zrangebyscore(RETRY_ZSET, 0, now())

    for raw in items:
        try:
            task = json.loads(raw)
            r.zrem(RETRY_ZSET, raw)
            r.xadd(TASK_STREAM, task)
        except:
            continue


def recover_orphans():
    try:
        pending = r.xpending_range(TASK_STREAM, GROUP, "-", "+", 10)

        for p in pending:
            msg_id = p["message_id"]

            entries = r.xrange(TASK_STREAM, msg_id, msg_id)
            if not entries:
                continue

            _, task = entries[0]

            set_state(task.get("task_id"), "recovered")

            r.xadd(TASK_STREAM, task)

    except:
        pass


def init_group():
    try:
        r.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
    except:
        pass


init_group()

print("LENTRA QUEUE LEVEL 5 ACTIVE (DISTRIBUTED SAFE MODE)")

last_recovery = 0

while True:
    try:
        drain_retry()

        if time.time() - last_recovery > 10:
            recover_orphans()
            last_recovery = time.time()

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
                process(task)
                r.xack(TASK_STREAM, GROUP, msg_id)

    except Exception as e:
        print("[FATAL]", str(e))
        time.sleep(2)
