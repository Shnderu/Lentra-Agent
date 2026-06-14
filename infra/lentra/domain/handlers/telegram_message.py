def handle(event: dict):

    # 🔥 FIX: поддержка старого и нового формата
    raw = event.get("raw") if isinstance(event, dict) else None
    if not raw:
        raw = event

    message = raw.get("message") if isinstance(raw, dict) else None
    if not message:
        return None

    text = message.get("text")
    chat_id = (message.get("chat") or {}).get("id")

    if not chat_id:
        return None

    if text == "/start":
        return {
            "chat_id": chat_id,
            "text": "👋 бот работает (pipeline ok)"
        }

    return {
        "chat_id": chat_id,
        "text": f"echo: {text}"
    }
