def classify_intent(task_type, payload, state=None):
    text = str(payload)

    # continuation logic (важно)
    if state and state.last_intent == "property_search":
        if "ещё" in text or "more" in text:
            return "property_pagination"

    if task_type == "telegram_message":
        if any(x in text.lower() for x in ["квартира", "rent", "аренда"]):
            return "property_search"

        if any(x in text.lower() for x in ["цена", "стоимость", "сколько"]):
            return "price_inquiry"

        return "chat"

    if task_type == "parse_property":
        return "property_search"

    if task_type == "ranking_event":
        return "analytics"

    return "fallback"
