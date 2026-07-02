from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine

engines = {}

engines["pricing"] = PricingEngine()

try:
    from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
    engines["risk"] = RiskEngine()
    print("[OK] risk loaded")
except Exception as e:
    print("[FAIL] risk:", e)

try:
    from lentra.core.market_intelligence.engines.signals_engine import SignalsEngine
    engines["signals"] = SignalsEngine()
    print("[OK] signals loaded")
except Exception as e:
    print("[FAIL] signals:", e)

try:
    from lentra.core.market_intelligence.engines.area_engine import AreaEngine
    engines["area"] = AreaEngine()
    print("[OK] area loaded")
except Exception as e:
    print("[FAIL] area:", e)

try:
    from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
    engines["dedup"] = DedupEngine()
    print("[OK] dedup loaded")
except Exception as e:
    print("[FAIL] dedup:", e)

print("\nENGINES ACTIVE:", list(engines.keys()))
