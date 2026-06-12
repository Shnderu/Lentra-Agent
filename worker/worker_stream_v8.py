import redis
import json
import time
import os

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
CONSUMER = f"worker-{os.getpid()}"

STATE_PREFIX = "task:state:"
LOCK_PREFIX = "task:lock:"

MAX_RETRY = 3


def now():
    return int(time.time())


def state_key(task_id):
    return f"{STATE_PREFIX}{task_id}"


def lock_key(task_id):
    return f"{LOCK_PREFIX}{task_id}"


def set_state(task_id, status, extra=None):
    payload = {
        "status": status,
        "updated_at": now()
    }
    if extra:
        payload.update(extra)

    r.hset(state_key(task_id), mapping=payload)


def get_retry(task):
    try:
        return int(task.get("retry", 0))
    except:
        return 0


def acquire_lock(task_id):
    return r.set(lock_key(task_id), "1", nx=True, ex=60)


def release_lock(task_id):
    r.delete(lock_key(task_id))


def handle(task):
    task_type = task.get("type")
    payload = task.get("payload", {})

    if task_type == "rent.search":
        city = payload.get("city", "unknown")

        time.sleep(0.2)

        return {
            "city": city,
            "hotels": 5,
            "avg_price": 1100,
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

    delay = min(2 ** retry, 30)
    run_at = now() + delay

    task["retry"] = retry + 1

    r.zadd(RETRY_ZSET, {
        json.dumps(task): run_at
    })

    set_state(task.get("task_id"), "retry_scheduled", {"run_at": run_at})


def process(task):
    task_id = task.get("task_id")

    set_state(task_id, "processing")

    if not acquire_lock(task_id):
        return

    try:
        result = handle(task)

        push_result(task_id, result)

        set_state(task_id, "done", {"result": json.dumps(result)})

    except Exception as e:
        set_state(task_id, "failed", {"error": str(e)})
        schedule_retry(task)

    finally:
        release_lock(task_id)


def drain_retry():
    items = r.zrangebyscore(RETRY_ZSET, 0, now())

    for raw in items:
        try:
            task = json.loads(raw)
            r.zrem(RETRY_ZSET, raw)
            r.xadd(TASK_STREAM, task)
        except:
            continue


def init_group():
    try:
        r.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
    except:
        pass


init_group()

print("LENTRA QUEUE LEVEL 4 ACTIVE (STATE MACHINE ENABLED)")

while True:
    try:
        drain_retry()

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
