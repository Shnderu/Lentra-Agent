def is_graph_enabled(context: dict = None) -> bool:
    """
    Feature toggle for graph_v2 system
    """

    context = context or {}

    # future: can be request-level routing
    return bool(context.get("graph_enabled", True))
