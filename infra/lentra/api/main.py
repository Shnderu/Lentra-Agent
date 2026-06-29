from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

app = FastAPI()

engine = MarketIntelligenceEngine()


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# WEBHOOK (Telegram)
# =========================
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    print("[TELEGRAM UPDATE]", data)

    return {"ok": True}


# =========================
# ANALYZE API (CORE ENGINE)
# =========================
class AnalyzeRequest(BaseModel):
    listings: List[Dict[str, Any]]
    query_text: Optional[str] = None


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    return engine.analyze(req.listings, req.query_text)


# =========================
# SEARCH API (LIGHT FILTER LAYER)
# =========================
class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(req: SearchRequest):
    # temporary minimal passthrough using engine pipeline
    fake_listing = [{"price": 700, "location": "beach", "risk": 0.5}]
    return engine.analyze(fake_listing, req.query)
