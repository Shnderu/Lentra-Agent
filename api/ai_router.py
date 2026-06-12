from fastapi import APIRouter
import redis
import json

router = APIRouter()
r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

@router.post("/route")
def route_intent(body: dict):
    intent = body["intent"]

    # SIMPLE RULE-BASED AI ROUTER (can be replaced with LLM later)
    if "rent" in intent:
        workflow = "rent.workflow.v1"
    elif "search" in intent:
        workflow = "search.workflow.v1"
    else:
        workflow = "default.workflow"

    wf_def = r.get(f"wf:defs:{workflow}")

    return {
        "intent": intent,
        "workflow": workflow,
        "definition_exists": wf_def is not None
    }
