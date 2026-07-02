from typing import Dict, Any


def attach_graph_layer(gateway, engines: Dict[str, Any]):
    """
    SAFE hook:
    НЕ влияет на bootstrap
    только enrich step (optional)
    """

    try:
        from lentra.core.market_intelligence.graph.integration import try_graph_execute

        def wrapped(payload: Dict[str, Any]):
            return try_graph_execute(engines, payload)

        gateway.graph_execute = wrapped

    except Exception:
        # FULL SAFETY: silent ignore
        pass

    return gateway
