import redis
import json
import time
import uuid
import os
import hashlib

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
# MULTI-TENANT CORE
# ----------------------------
TENANT_PREFIX = "tenant:"
API_KEY_PREFIX = "apikey:"
RATE_PREFIX = "rate:"
BILLING_PREFIX = "billing:"
QUEUE_PREFIX = "queue:"
WF_PREFIX = "wf:"
STATE_PREFIX = "task:state:"

TASK_STREAM = "stream:rent:tasks"

# ----------------------------
# AUTH / API KEYS
# ----------------------------
def generate_api_key(tenant_id):
    raw = f"{tenant_id}:{uuid.uuid4().hex}"
    key = hashlib.sha256(raw.encode()).hexdigest()

    r.hset(f"{API_KEY_PREFIX}{key}", mapping={
        "tenant_id": tenant_id,
        "created_at": int(time.time())
    })

    return key


def validate_api_key(api_key):
    data = r.hgetall(f"{API_KEY_PREFIX}{api_key}")
    return data.get("tenant_id") if data else None


# ----------------------------
# RATE LIMITING (TOKEN BUCKET)
# ----------------------------
def rate_limit(tenant_id):
    key = f"{RATE_PREFIX}{tenant_id}"
    bucket = r.hgetall(key)

    now = int(time.time())
    capacity = 10
    refill_rate = 1  # per second

    tokens = float(bucket.get("tokens", capacity))
    last = int(bucket.get("ts", now))

    elapsed = now - last
    tokens = min(capacity, tokens + elapsed * refill_rate)

    if tokens < 1:
        return False

    tokens -= 1

    r.hset(key, mapping={
        "tokens": tokens,
        "ts": now
    })

    return True


# ----------------------------
# BILLING ENGINE (PER TASK COST)
# ----------------------------
def charge(tenant_id, task_type):
    cost_map = {
        "rent.search": 1,
        "enrich.ai": 2,
        "filter.rules": 1
    }

    cost = cost_map.get(task_type, 1)

    r.hincrby(f"{BILLING_PREFIX}{tenant_id}", "credits_used", cost)

    return cost


# ----------------------------
# TENANT QUEUE ISOLATION
# ----------------------------
def get_tenant_queue(tenant_id):
    return f"{QUEUE_PREFIX}{tenant_id}:tasks"


def enqueue_task(tenant_id, task):
    stream = get_tenant_queue(tenant_id)

    r.xadd(stream, task)


# ----------------------------
# WORKFLOW ENGINE (MULTI-TENANT)
# ----------------------------
def get_workflow(tenant_id, task_id):
    raw = r.get(f"{WF_PREFIX}{tenant_id}:{task_id}")
    if raw:
        return json.loads(raw)

    wf = {
        "version": "v2",
        "current": "step_0",
        "steps": [
            {"name": "step_0", "type": "rent.search"},
            {"name": "ai_enrich", "type": "enrich.ai"},
            {"name": "filter", "type": "filter.rules"}
        ]
    }

    r.set(f"{WF_PREFIX}{tenant_id}:{task_id}", json.dumps(wf))
    return wf


def save_workflow(tenant_id, task_id, wf):
    r.set(f"{WF_PREFIX}{tenant_id}:{task_id}", json.dumps(wf))


# ----------------------------
# CORE EXECUTION
# ----------------------------
def process_task(tenant_id, task):
    task_id = task["task_id"]
    task_type = task["type"]

    if not rate_limit(tenant_id):
        return {"error": "rate_limited"}

    charge(tenant_id, task_type)

    wf = get_workflow(tenant_id, task_id)

    # simple step execution
    if task_type == "rent.search":
        result = {
            "city": task["payload"].get("city"),
            "price_index": 1200,
            "hotels": 8
        }

    elif task_type == "enrich.ai":
        result = {
            **task.get("result", {}),
            "ai_score": 0.91
        }

    else:
        result = {"ok": True}

    # advance workflow
    if wf["current"] == "step_0":
        wf["current"] = "ai_enrich"
    elif wf["current"] == "ai_enrich":
        wf["current"] = "filter"
    else:
        wf["current"] = "done"

    save_workflow(tenant_id, task_id, wf)

    # persist state
    r.hset(f"{STATE_PREFIX}{task_id}", mapping={
        "tenant_id": tenant_id,
        "status": wf["current"],
        "updated_at": int(time.time())
    })

    return result


# ----------------------------
# BILLING INSPECTION
# ----------------------------
def get_billing(tenant_id):
    return r.hgetall(f"{BILLING_PREFIX}{tenant_id}")


# ----------------------------
# SIMPLE CONTROL API (SIMULATED)
# ----------------------------
def create_tenant(name):
    tenant_id = str(uuid.uuid4())

    r.hset(f"{TENANT_PREFIX}{tenant_id}", mapping={
        "name": name,
        "created_at": int(time.time())
    })

    return tenant_id


# ----------------------------
# DEMO ENTRYPOINT
# ----------------------------
if __name__ == "__main__":
    print("LENTRA LEVEL 8 SAAS PLATFORM ACTIVE")

    # demo tenant
    tenant = create_tenant("default")

    api_key = generate_api_key(tenant)

    print("TENANT:", tenant)
    print("API KEY:", api_key)

    while True:
        time.sleep(5)
        billing = get_billing(tenant)
        print("[BILLING]", billing)
