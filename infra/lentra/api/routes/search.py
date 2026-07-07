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

        engine_keys = []

        if hasattr(pipeline, "mi_engine"):
            engine_keys = [
                "market_intelligence"
            ]

        elif hasattr(pipeline, "_engine_keys"):
            engine_keys = pipeline._engine_keys

        return {
            "status": "ok",
            "engine_keys": engine_keys,
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }
