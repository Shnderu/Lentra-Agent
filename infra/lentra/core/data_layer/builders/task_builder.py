def build_task(payload):
    """
    V3 SAFE TASK BUILDER
    """

    if isinstance(payload, str):
        payload = {"title": payload}

    if not isinstance(payload, dict):
        payload = {"title": str(payload)}

    return {
        "query": payload.get("title", ""),
        "raw": payload
    }
