from fastapi import APIRouter
import traceback

from lentra.api.pipeline import run_pipeline
from lentra.api.pipeline import get_pipeline

router = APIRouter()


@router.post("/search")
def search(payload: dict):

    try:
        result = run_pipeline(payload)

        pipeline = get_pipeline()

        return {
            "status": "ok",
            "engine_keys": pipeline["gateway"]._engine_keys,
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }
