from fastapi import APIRouter
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)

engine = MarketIntelligenceEngine()


@router.post("")
def feedback(payload: dict):

    listing = payload.get("listing")
    action = payload.get("action")

    if listing and action:
        engine.decision.feedback(listing, action)

    return {
        "status": "ok",
        "learning": True
    }
