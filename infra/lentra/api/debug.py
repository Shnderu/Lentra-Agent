from fastapi import APIRouter
from lentra.core.market_intelligence.visibility.visibility_layer import VisibilityLayer

router = APIRouter()

# singleton visibility (важно для runtime)
viz = VisibilityLayer()


@router.get("/debug/events")
def get_events():
    return viz.snapshot()


@router.post("/debug/clear")
def clear():
    viz.stream.clear()
    return {"status": "cleared"}
