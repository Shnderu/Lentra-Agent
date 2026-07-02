def assert_engine_contract(result: dict):
    """
    FAIL FAST CONTRACT GUARANTEE
    """

    if "graph" in result:
        raise RuntimeError("ENGINE VIOLATION: graph field detected")


    return True
