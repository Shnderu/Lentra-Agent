from dataclasses import dataclass


@dataclass(frozen=True)
class RoutingMapLock:
    """
    ARCH V2 MARKET INTELLIGENCE AUTHORITY LOCK

    Canonical intelligence ownership:

    Pricing:
        Market Intelligence PricingEngine

    Dedup:
        Market Intelligence DedupIndex V4 pipeline

    Risk:
        Market Intelligence RiskEngine

    This file defines architectural ownership only.
    Runtime adapters remain responsible for Data Layer compatibility.
    """

    pricing_engine: str = (
        "lentra.core.market_intelligence.engines.pricing_engine.PricingEngine"
    )

    dedup_engine: str = (
        "lentra.core.market_intelligence.dedup.dedup_index.DedupIndex"
    )

    risk_engine: str = (
        "lentra.core.market_intelligence.engines.risk_engine.RiskEngine"
    )

    expat_engine: str = (
        "lentra.core.market_intelligence.expat.expat_score_engine.ExpatScoreEngine"
    )


    legacy_dedup_adapter: str = "legacy::removed"
    legacy_pricing_adapter: str = "legacy::removed"


    core_v2_enabled: bool = False
    pricing_v1_enabled: bool = False
    dedup_v1_enabled: bool = False
