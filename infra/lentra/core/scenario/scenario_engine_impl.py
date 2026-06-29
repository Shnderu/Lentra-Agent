
def scenario_engine_impl(node, state):
    """
    Temporary safe fallback implementation.
    Prevents runtime crash while scenario layer is not implemented.
    """

    return type("Result", (), {
        "data": {},
        "next": []
    })()
