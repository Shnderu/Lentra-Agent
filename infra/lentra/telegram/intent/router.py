def detect_intent(state: dict, payload: dict, callback: str):
    """
    Очень простой intent router (MVP без ML)
    """

    screen = state.get("screen", "start")
    source = payload.get("source")

    # 1. фильтрация UX контекста
    if callback == "filter" or source == "state_filter":
        return "FILTER_INTENT"

    # 2. уточнение
    if callback == "refine" or source == "state_refine":
        return "REFINE_INTENT"

    # 3. если пользователь на экране property_list
    if screen == "property_list":
        return "BROWSE_INTENT"

    # 4. fallback
    return "DEFAULT_INTENT"
