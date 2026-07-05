from fastapi import APIRouter
from lentra.api.pipeline import get_pipeline

router = APIRouter()


@router.post("/search")
def search(payload: dict):
    pipeline = get_pipeline()
    gateway = pipeline["gateway"]

    try:
        result = gateway.compute(payload)

        response = {
            "status": "ok",
            "engine_keys": gateway.get_engine_keys(),
            **result
        }

        # HARD GUARANTEE: single JSON response only
        return response

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "engine_keys": gateway.get_engine_keys()
        }
