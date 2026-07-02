"""
ENGINE RESTORE LAYER

SAFE RULE:
- never breaks pricing engine
- fails gracefully per module
- logs missing modules clearly
"""

from typing import Dict, Any


def load_engines() -> Dict[str, Any]:
    engines: Dict[str, Any] = {}

    # CORE
    try:
        from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine
        engines["pricing"] = PricingEngine()
    except Exception as e:
        print("[ENGINE] pricing failed:", e)

    # RISK
    try:
        from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
        engines["risk"] = RiskEngine()
    except Exception as e:
        print("[ENGINE] risk missing:", e)

    # SIGNALS
    try:
        from lentra.core.market_intelligence.engines.signals_engine import SignalsEngine
        engines["signals"] = SignalsEngine()
    except Exception as e:
        print("[ENGINE] signals missing:", e)

    # AREA
    try:
        from lentra.core.market_intelligence.engines.area_engine import AreaEngine
        engines["area"] = AreaEngine()
    except Exception as e:
        print("[ENGINE] area missing:", e)

    # DEDUP
    try:
        from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
        engines["dedup"] = DedupEngine()
    except Exception as e:
        print("[ENGINE] dedup missing:", e)

    print("[ENGINE] ACTIVE:", list(engines.keys()))
    return engines
