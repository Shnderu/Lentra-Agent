from typing import Any, Dict
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

_engine = MarketIntelligenceEngine()

def interpret(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _engine.analyze(payload)
