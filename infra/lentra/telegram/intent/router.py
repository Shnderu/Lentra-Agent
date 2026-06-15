from lentra.api.search.router import search_endpoint


def route(chat_id, event):
    """
    v5.1: unified API routing layer
    """

    if event.get("type") == "search":
        return search_endpoint(event.get("payload", {}))

    return {"ok": True, "message": "no-op"}
