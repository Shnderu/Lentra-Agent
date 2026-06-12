from fastapi import APIRouter
import uuid

router = APIRouter()

@router.post("/ai/workflow")
def generate_workflow(body: dict):
    intent = body["intent"]

    # pseudo-AI generator
    if "rent" in intent:
        steps = [
            {"name": "search", "type": "rent.search"},
            {"name": "enrich", "type": "ai.enrich"},
            {"name": "rank", "type": "ai.rank"}
        ]
    else:
        steps = [
            {"name": "fetch", "type": "generic.fetch"},
            {"name": "process", "type": "generic.process"}
        ]

    wf = {
        "id": str(uuid.uuid4()),
        "steps": steps
    }

    return wf
