from fastapi import APIRouter
import redis
import json
import uuid
import time

router = APIRouter()
r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

@router.post("/wf/register")
def register_workflow(body: dict):
    name = body["name"]
    definition = body["definition"]

    r.set(f"wf:defs:{name}", json.dumps(definition))

    return {"status": "registered", "name": name}


@router.post("/wf/start")
def start_workflow(body: dict):
    name = body["name"]
    input_data = body.get("input", {})

    wf_id = str(uuid.uuid4())

    definition = json.loads(r.get(f"wf:defs:{name}"))

    r.hset(f"wf:run:{wf_id}", mapping={
        "name": name,
        "status": "running",
        "created_at": time.time(),
        "input": json.dumps(input_data)
    })

    # emit start event
    r.xadd("stream:events", {
        "type": "workflow_started",
        "wf_id": wf_id,
        "name": name
    })

    # schedule first step
    first = definition["start"]

    r.xadd("stream:wf:tasks", {
        "wf_id": wf_id,
        "step": first,
        "input": json.dumps(input_data)
    })

    return {"wf_id": wf_id, "status": "started"}
