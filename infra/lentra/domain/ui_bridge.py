def handle_screen(screen: str, event: dict) -> dict:
    text = (event.get("text") or "").strip()

    # =========================
    # RENT FLOW
    # =========================
    if screen == "rent":
        return {
            "text": "🏠 Аренда\nВведите город или район для поиска."
        }

    # =========================
    # SEARCH FLOW
    # =========================
    if screen == "search":
        return {
            "text": "🔎 Поиск\nВведите запрос:"
        }

    # =========================
    # ALERTS FLOW
    # =========================
    if screen == "alerts":
        return {
            "text": "📊 Уведомления\nНастройка алертов цен."
        }

    # =========================
    # PROFILE FLOW
    # =========================
    if screen == "profile":
        return {
            "text": "👤 Профиль\nИнформация пользователя."
        }

    return {
        "text": "Неизвестный сценарий"
    }
