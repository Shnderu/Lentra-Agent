from lentra.core.graph.node import GraphNode
from lentra.core.handlers import (
    rent_intelligence_handler,
    rent_fetch_handler,
    rent_aggregate_handler,
    response_handler
)


def build_graph():

    graph = {}

    graph["INTENT"] = GraphNode(
        name="INTENT",
        handler=rent_intelligence_handler,
        next_node="FETCH"
    )

    graph["FETCH"] = GraphNode(
        name="FETCH",
        handler=rent_fetch_handler,
        next_node="AGGREGATE"
    )

    graph["AGGREGATE"] = GraphNode(
        name="AGGREGATE",
        handler=rent_aggregate_handler,
        next_node="RESPONSE"
    )

    graph["RESPONSE"] = GraphNode(
        name="RESPONSE",
        handler=response_handler,
        next_node=None
    )

    return graph
