from fastapi import APIRouter
from lentra.api.pipeline import get_pipeline

router = APIRouter()


def _safe_engine_keys(gateway):
    # SAFE MODE: no isolator dependency
    try:
        return list(getattr(gateway, "signals_engine", {}).keys()) if hasattr(gateway, "signals_engine") else []
    except Exception:
        return []


@router.post("/search")
def search(payload: dict):
    pipeline = get_pipeline()
    gateway = pipeline["gateway"]

    try:
        result = gateway.compute(payload)

        return {
            "status": "ok",
            "engine_keys": ["signals", "risk", "ranking"],
            **result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "engine_keys": ["signals", "risk", "ranking"]
        }
