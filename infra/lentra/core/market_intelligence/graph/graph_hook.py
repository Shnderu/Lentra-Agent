from lentra.core.market_intelligence.graph.intelligence_graph_runtime import IntelligenceGraphRuntime

_graph = IntelligenceGraphRuntime()


def attach_graph_layer(response: dict, engines: dict, payload: dict) -> dict:
    """
    SAFE NON-BREAKING HOOK

    если падает → игнорируем
    """

    try:
        if not _graph.enabled:
            return response

        return _graph.run(response, payload)

    except Exception:
        # CRITICAL: never break API
        return response
