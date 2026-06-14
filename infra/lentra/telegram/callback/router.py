def handle_callback(data: str):

    if not data:
        return {"ok": False}

    if data.startswith("open:"):
        item_id = data.split(":")[1]
        return {
            "ok": True,
            "action": "open",
            "id": item_id
        }

    if data.startswith("save:"):
        item_id = data.split(":")[1]
        return {
            "ok": True,
            "action": "save",
            "id": item_id
        }

    return {
        "ok": False,
        "error": "unknown_callback"
    }
