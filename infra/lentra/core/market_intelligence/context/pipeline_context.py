from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet


@dataclass(frozen=True)
class SignalContext:
    pricing: Dict[str, Any]
    area: Dict[str, Any]
    dedup: Dict[str, Any]


@dataclass(frozen=True)
class RiskContext:
    risk_level: float
    score: float
    level: str
    components: Dict[str, Any]


@dataclass(frozen=True)
class RankingContext:
    score: float
    components: Dict[str, Any]
    version: str = "ranking_v2"


@dataclass(frozen=True)
class EnrichmentView:
    market_context: str
    recommendation_hint: str
    meta: Dict[str, Any]


@dataclass(frozen=True)
class PipelineContext:
    raw: Dict[str, Any]
    signals: SignalContext
    risk: RiskContext
    ranking: RankingContext
    enrichment: EnrichmentView
