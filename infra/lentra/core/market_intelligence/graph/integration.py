from typing import Dict, Any


def try_graph_execute(engines: Dict[str, Any], payload: Dict[str, Any]):
    """
    SAFE wrapper:
    - если graph есть → используем
    - если упал → fallback на direct engines
    """

    try:
        from lentra.core.market_intelligence.graph.intelligence_graph_runtime import (
            IntelligenceGraphRuntime
        )

        graph = IntelligenceGraphRuntime()
        return graph.execute(engines, payload)

    except Exception:
        # CRITICAL SAFETY FALLBACK
        # никогда не ломаем API
        return {
            "graph_version": "fallback",
            "results": {
                "pricing": engines.get("pricing", {}).evaluate(payload) if "pricing" in engines else None,
                "signal": engines.get("signal", {}).evaluate(payload) if "signal" in engines else None
            }
        }
