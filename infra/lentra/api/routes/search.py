from fastapi import APIRouter
import traceback

from lentra.api.pipeline import get_pipeline
from lentra.core.observability.trace_store import trace_store

router = APIRouter()

@router.post("/search")
def search(payload: dict):
    pipeline = get_pipeline()
    gateway = pipeline["gateway"]

    try:
        result = gateway.compute(payload)

        request_id = result.get("request_id")

        return {
            "status": "ok",
            "request_id": request_id,
            "engine_keys": pipeline["gateway"]._engine_keys if hasattr(pipeline["gateway"], "_engine_keys") else [],
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }


@router.get("/debug/traces/{request_id}")
def get_trace(request_id: str):
    return {
        "status": "ok",
        "request_id": request_id,
        "trace": trace_store.get(request_id)
    }
