from fastapi import APIRouter
from lentra.api.pipeline import get_pipeline

router = APIRouter(prefix="/admin")


@router.get("/engines")
def list_engines():
    pipeline = get_pipeline()
    return {
        "engines": ["signals", "risk", "ranking"]
    }
