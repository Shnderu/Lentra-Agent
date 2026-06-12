from fastapi import APIRouter
import redis
import time
import uuid
import json

router = APIRouter()
r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM = "stream:wf:tasks"

@router.post("/workflow")
def create_workflow():
    wf_id = str(uuid.uuid4())

    workflow = {
        "id": wf_id,
        "status": "running",
        "created_at": time.time()
    }

    # пример DAG для rent.search pipeline
    steps = {
        "fetch": {
            "type": "rent.search",
            "depends_on": []
        },
        "enrich": {
            "type": "ai.enrich",
            "depends_on": ["fetch"]
        },
        "rank": {
            "type": "ai.rank",
            "depends_on": ["enrich"]
        }
    }

    r.hset(f"wf:{wf_id}", mapping=workflow)
    r.set(f"wf:{wf_id}:steps", json.dumps(steps))

    # стартуем root steps
    for step_id, step in steps.items():
        if not step["depends_on"]:
            r.xadd(STREAM, {
                "wf_id": wf_id,
                "step_id": step_id,
                "type": step["type"],
                "status": "queued"
            })

    return {"workflow_id": wf_id, "status": "started"}
