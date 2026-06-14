def build_telegram_message(ux):
    if not ux or not isinstance(ux, dict):
        return {"text": "", "keyboard": []}

    text = ux.get("telegram_text") or ux.get("text") or ""
    actions = ux.get("ux", {}).get("actions", [])

    keyboard = []

    for a in actions:
        if isinstance(a, dict):
            keyboard.append({
                "text": a.get("label", ""),
                "callback_data": a.get("type", "")
            })

    return {
        "text": text,
        "keyboard": keyboard
    }
