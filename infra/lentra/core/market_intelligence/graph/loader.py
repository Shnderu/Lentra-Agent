from typing import Any, Optional


def try_load_graph_engine() -> Optional[Any]:
    """
    SAFE PLUGIN LOADER

    Graph layer is OPTIONAL.
    Never breaks bootstrap.
    """

    try:
        from lentra.core.market_intelligence.graph.intelligence_graph_runtime import (
            IntelligenceGraphRuntime
        )

        return IntelligenceGraphRuntime()

    except Exception as e:
        # SAFE FALLBACK
        # graph is non-critical enrichment layer
        print(f"[GRAPH][WARN] disabled due to: {e}")
        return None
