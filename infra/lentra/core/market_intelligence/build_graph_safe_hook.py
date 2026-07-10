from typing import Dict, Any


def attach_graph_layer(gateway, engines: Dict[str, Any]):

    """
    Optional graph enrichment attachment.

    Does not modify runtime pipeline.
    """

    def graph_enrichment(payload: Dict[str, Any]):

        from lentra.core.market_intelligence.graph.integration import (
            GraphIntegration
        )

        return GraphIntegration().build(payload)

    gateway.graph_enrichment = graph_enrichment

    return gateway
