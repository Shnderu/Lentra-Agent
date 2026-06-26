from lentralication.search.pipeline import execute_search


def route(chat_id, event):
    """
    TRANSPORT LAYER ONLY
    """

    event_type = event.get("type")

    if event_type == "search":
        return execute_search(event.get("payload", {}), state=event.get("state"))

    return {
        "ok": True,
        "type": "noop"
    }
