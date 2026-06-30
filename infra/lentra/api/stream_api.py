from fastapi import APIRouter
from lentra.core.market_intelligence.stream.global_stream import get_stream

router = APIRouter()

stream = get_stream()


@router.get("/debug/stream")
def debug_stream():
    """
    simple snapshot of subscribers state
    """
    return {
        "subscribers": len(stream.subscribers)
    }
