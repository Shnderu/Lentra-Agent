from fastapi import APIRouter

router = APIRouter(prefix="/admin")


@router.get("/engines")
def list_engines():
    return {
        "engines": ["signals", "risk", "ranking", "enrichment"]
    }
