from pydantic import BaseModel
from typing import Dict, List, Optional, Literal


# =========================
# INPUT CONTRACT
# =========================

class SearchRequest(BaseModel):
    query: str
    price: float
    market_price: float


# =========================
# SIGNALS OUTPUT CONTRACT
# =========================

class PricingSignal(BaseModel):
    score: float
    direction: Literal["over", "under", "neutral"]
    deviation: float


class AreaSignal(BaseModel):
    score: float
    note: Optional[str] = None


class DedupSignal(BaseModel):
    score: float
    confidence: float


class SignalsOutput(BaseModel):
    pricing: PricingSignal
    area: AreaSignal
    dedup: DedupSignal


# =========================
# COUPLING CONTRACT
# =========================

class CouplingOutput(BaseModel):
    score: float
    factors: Dict[str, float]


# =========================
# RISK CONTRACT
# =========================

class RiskComponents(BaseModel):
    price_risk: float
    area_risk: float
    duplication: float
    heuristic: float
    coupling: float
    anti_scam_overlay: float
    base_risk: float


class RiskOutput(BaseModel):
    risk_level: float
    score: float
    level: Literal["low", "medium", "high"]
    components: RiskComponents


# =========================
# RANKING CONTRACT
# =========================

class RankingComponents(BaseModel):
    price_quality: float
    area_quality: float
    risk_penalty: float
    coupling_penalty: float
    dedup_confidence: float


class RankingOutput(BaseModel):
    score: float
    components: RankingComponents
    version: str = "ranking_v2"


# =========================
# FINAL RESPONSE CONTRACT
# =========================

class IntelligenceResponse(BaseModel):
    engine_keys: List[str]

    pricing: PricingSignal
    area: AreaSignal
    dedup: DedupSignal

    coupling: CouplingOutput
    risk: RiskOutput
    ranking: RankingOutput
