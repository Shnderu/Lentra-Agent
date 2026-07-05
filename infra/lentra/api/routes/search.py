from fastapi import APIRouter, Body
import traceback

from lentra.api.pipeline import get_pipeline

router = APIRouter()


@router.post("/search")
def search(payload: dict = Body(...)):
    pipeline = get_pipeline()
    gateway = pipeline["gateway"]

    try:
        result = gateway.compute(payload)

        return {
            "status": "ok",
            "engine_keys": pipeline["gateway"]._engine_keys if hasattr(pipeline["gateway"], "_engine_keys") else [],
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }
