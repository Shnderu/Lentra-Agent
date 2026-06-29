from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
def search(q: str):
    """
    DISABLED LEGACY ENDPOINT
    Forwarding removed to prevent shadow routing.
    """
    return {
        "query": q,
        "total": 0,
        "objects": [],
        "error": "legacy endpoint disabled"
    }
