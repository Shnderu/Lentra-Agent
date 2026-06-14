def handle(payload):
    text = payload.get("text", "")
    chat_id = payload.get("chat_id")

    if not text:
        return {
            "type": "intent.empty",
            "chat_id": chat_id,
            "payload": payload
        }

    text = text.strip()

    # COMMANDS LAYER
    if text.startswith("/start"):
        return {
            "type": "command.start",
            "chat_id": chat_id,
            "payload": {
                "screen": "start",
                "raw": text
            }
        }

    if text.startswith("/help"):
        return {
            "type": "command.help",
            "chat_id": chat_id,
            "payload": {
                "screen": "help",
                "raw": text
            }
        }

    if text.startswith("/"):
        return {
            "type": "command.unknown",
            "chat_id": chat_id,
            "payload": {
                "raw": text
            }
        }

    # INTENT LAYER
    if "rent" in text.lower() or "rent" in text.lower():
        return {
            "type": "intent.property_search",
            "chat_id": chat_id,
            "payload": payload
        }

    return {
        "type": "intent.text",
        "chat_id": chat_id,
        "payload": payload
    }
