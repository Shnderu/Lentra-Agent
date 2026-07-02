from lentra.core.market_intelligence.graph.graph_hook import attach_graph_layer


def apply_graph_layer(gateway, engines, payload, response):
    """
    SAFE wrapper
    """

    return attach_graph_layer(response, engines, payload)
