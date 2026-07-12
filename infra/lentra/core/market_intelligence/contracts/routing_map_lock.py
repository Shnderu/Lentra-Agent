from dataclasses import dataclass

@dataclass(frozen=True)
class RoutingMapLock:
    pricing_engine: str = "lentra.core.market.pricing_engine.PricingEngine"
    dedup_engine: str = "lentra.core.market_intelligence.dedup.unified_dedup_engine.UnifiedDedupEngine"
    risk_engine: str = "lentra.core.market_intelligence.engines.risk_engine.RiskEngine"
    expat_engine: str = "lentra.core.market_intelligence.expat.expat_score_engine.ExpatScoreEngine"

    legacy_dedup_adapter: str = "legacy::removed"
    legacy_pricing_adapter: str = "legacy::removed"

    core_v2_enabled: bool = False
    pricing_v1_enabled: bool = False
    dedup_v1_enabled: bool = False
